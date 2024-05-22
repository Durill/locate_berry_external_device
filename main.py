from pathlib import Path
from typing import Tuple
from uuid import uuid4

import httpx
from httpx import Client
from time import sleep

from helpers.logger import CustomLogger
from helpers.request_sender import RequestSender
from requests.synchronous import SynchronousRequest
from settings import Settings


if __name__ == '__main__':
    logger = CustomLogger()
    settings = Settings(logger=logger)
    client = httpx.Client()
    synchronous_request = SynchronousRequest(server_url=settings.SERVER_URL, client=client)
    request_sender = RequestSender(synchronous_request=synchronous_request)

    while not settings.SYSTEM_CHECKED:

        try:

            if request_sender.health_check() != 200:
                logger.log_to_file_and_screen("Server not responding properly, hitting again in 5 seconds...")
                sleep(5)
                continue

            if settings.checking_device_settings():
                settings.set_values_from_file()
                logger.log_to_file_and_screen("Device configured properly!")
            else:
                register_parameters = request_sender.register_device()
                settings.register_and_bind_device(register_parameters=register_parameters)
                logger.log_to_file_and_screen("Device registered properly!")

            settings.SYSTEM_CHECKED = True

        except httpx.HTTPError as error:
            print(f"HTTP Exception for {error.request.url} - {error}")
            sleep(5)

    print("\n--- Preparing for localization transmission ---\n")
    while settings.TRANSMITTING:
        print("Transmitting Trip localization")
        sleep(7)

    client.close()
