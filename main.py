from pathlib import Path
from typing import Tuple
from uuid import uuid4

import httpx
from httpx import Client
from time import sleep
from settings import settings


def perform_health_check(http_client: Client) -> int:
    return http_client.get(f"{settings.SERVER_URL}/api/health-check/").status_code


def register_device_on_server(http_client: Client) -> Tuple[bool, str]:
    settings.DEVICE_ID = str(uuid4())

    payload = {
        "device_id": settings.DEVICE_ID,
        "device_name": settings.DEVICE_NAME,
        "user_email": settings.OWNER_EMAIL,
    }

    response = http_client.post(f"{settings.SERVER_URL}/device/api/register/", data=payload)
    if response.status_code == 201:
        settings.IS_REGISTERED = True
    return settings.IS_REGISTERED, settings.DEVICE_ID


def write_const_to_file():
    base_dir = Path(__file__).resolve()
    if not Path(base_dir.with_name("id.txt")).is_file():
        print('no such file, generating file...')
        with (open('id.txt', 'w') as file):
            payload = f"DEVICE_ID={settings.DEVICE_ID}\nIS_REGISTERED={settings.IS_REGISTERED}\nOWNER_EMAIL={settings.OWNER_EMAIL}"
            file.write(str(payload))

    else:
        print('yeah, file found')
        file_dict: dict = {}
        with open('id.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                split_list = line.split('=', )
                file_dict[split_list[0]] = split_list[1].replace('\n', '')
            print(file_dict)


if __name__ == '__main__':

    client = httpx.Client()
    while settings.SYSTEMS_CHECK:

        try:
            write_const_to_file()

            # if perform_health_check(http_client=client) != 200:
            #     print(
            #         "Server not responding properly, ",
            #         "device will try to hit server with request again but who know what will happen"
            #     )
            #     sleep(5)
            #     continue
            #
            # if not Settings.IS_REGISTERED and not Settings.DEVICE_ID:
            #     Settings.IS_REGISTERED, Settings.DEVICE_ID = register_device_on_server(http_client=client)

            settings.SYSTEMS_CHECK = False

        except httpx.HTTPError as error:
            print(f"HTTP Exception for {error.request.url} - {error}")
            sleep(5)
    client.close()

    print("\n--- Preparing for geometry transmission ---\n")
    while settings.TRANSMITTING:
        print("Transmitting Trip geometry")
        sleep(7)
