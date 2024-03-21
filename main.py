from pathlib import Path
from typing import Tuple
from uuid import uuid4

import httpx
from httpx import Client
from time import sleep

from requests.synchronous import SynchronousRequests
from settings import Settings
from logger import CustomLogger


if __name__ == '__main__':
    logger = CustomLogger()
    settings = Settings(logger=logger)
    client = httpx.Client()
    synchronous_requests = SynchronousRequests(server_url=settings.SERVER_URL, client=client)

    while settings.SYSTEMS_CHECK:

        try:
            settings.checking_and_setting_device_settings()

            if synchronous_requests.perform_health_check() != 200:
                logger.log_to_file_and_screen("Server not responding properly, hitting again in 5 seconds...")
                sleep(5)
                continue

            if not settings.IS_REGISTERED:
                if synchronous_requests.register_device(
                    device_id=settings.DEVICE_ID,
                    device_name=settings.DEVICE_NAME,
                    owner_email=settings.OWNER_EMAIL,
                ) == 201:
                    logger.log_to_file_and_screen("Device registered properly!")
                    settings.IS_REGISTERED = True
                else:
                    logger.log_to_file_and_screen("Server not responding properly, hitting again in 5 seconds...")
                    sleep(5)
                    continue

            settings.SYSTEMS_CHECK = False

        except httpx.HTTPError as error:
            print(f"HTTP Exception for {error.request.url} - {error}")
            sleep(5)
    client.close()

    print("\n--- Preparing for geometry transmission ---\n")
    while settings.TRANSMITTING:
        print("Transmitting Trip geometry")
        sleep(7)
