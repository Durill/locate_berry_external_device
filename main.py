from datetime import datetime

import httpx
from time import sleep

from helpers.logger import CustomLogger
from helpers.request_sender import RequestSender
from helpers.utils import get_new_authorization
from localization import Localization
from requests.synchronous import SynchronousRequest
from settings import Settings


if __name__ == '__main__':
    logger = CustomLogger()
    settings = Settings(logger=logger)
    client = httpx.Client()
    synchronous_request = SynchronousRequest(server_url=settings.SERVER_URL, client=client)
    request_sender = RequestSender(synchronous_request=synchronous_request)
    localization = Localization(logger=logger)
    localization.set_and_power_module()

    while not settings.SYSTEM_CHECKED:

        try:

            if request_sender.health_check() != 200:
                logger.log_to_file_and_screen("Server not responding properly, hitting again in 5 seconds...")
                sleep(5)
                continue

            if settings.checking_device_settings():
                settings.set_values_from_file()
                tokens = request_sender.get_tokens(
                    device_id=settings.DEVICE_ID,
                    password=settings.PASSWORD,
                )
                settings.set_new_tokens(
                    access_token=tokens['access_token'],
                    refresh_token=tokens['refresh_token']
                )
                logger.log_to_file_and_screen("Device configured properly!")
            else:
                register_parameters = request_sender.register_device()
                settings.register_and_bind_device(register_parameters=register_parameters)
                tokens = request_sender.get_tokens(
                    device_id=settings.DEVICE_ID,
                    password=settings.PASSWORD,
                )
                settings.set_new_tokens(
                    access_token=tokens['access_token'],
                    refresh_token=tokens['refresh_token']
                )
                logger.log_to_file_and_screen("Device registered properly!")

            settings.SYSTEM_CHECKED = True

        except httpx.HTTPError as error:
            logger.log_to_file_and_screen(f"HTTP Exception for {error.request.url} - {error}")
            sleep(5)
        except Exception as error:
            logger.log_to_file_and_screen(f"Exception: {error}")
            sleep(5)

    logger.log_to_file_and_screen(f"\n--- Preparing for localization transmission at {datetime.now()} ---\n")
    while settings.TRANSMITTING:
        try:
            start_time = datetime.now()
            localization_points = localization.get_actual_localization()
            geometry = {
                "type": "LineString",
                "coordinates": [
                    [localization_points[0].longitude, localization_points[0].latitude],
                    [localization_points[1].longitude, localization_points[1].latitude],
                    [localization_points[2].longitude, localization_points[2].latitude],
                ]
            }

            if not localization.previous_update_ending_point:
                result = request_sender.create_trip(
                    geometry=geometry,
                    device_id=settings.DEVICE_ID,
                    access_token=settings.ACCESS_TOKEN
                )
                if result['status_code'] == 200:
                    settings.TRIP_ID = result['trip_id']
                elif result['status_code'] == 401:
                    get_new_authorization(
                        request_sender=request_sender,
                        settings=settings,
                        logger=logger
                    )
                else:
                    raise httpx.HTTPError

            else:
                result = request_sender.update_trip(
                    geometry=geometry,
                    device_id=settings.DEVICE_ID,
                    trip_id=settings.TRIP_ID,
                    access_token=settings.ACCESS_TOKEN
                )
                if result['status_code'] == 401:
                    get_new_authorization(
                        request_sender=request_sender,
                        settings=settings,
                        logger=logger
                    )
                elif result['status_code'] != 200:
                    raise httpx.HTTPError

            localization.previous_update_ending_point = localization_points[2]

            end_time = datetime.now()
            passed_time = 10 - (end_time - start_time).seconds
            if passed_time > 0:
                sleep(passed_time)

        except httpx.HTTPError as error:
            logger.log_to_file_and_screen(f"HTTP Exception for {error.request.url} - {error}")
            sleep(5)
        except ConnectionError as error:
            logger.log_to_file_and_screen(f"Connection Error: {error}")
            sleep(5)
        except Exception as error:
            logger.log_to_file_and_screen(f"Exception: {error}")
            sleep(5)

    client.close()
