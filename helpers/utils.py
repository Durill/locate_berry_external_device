from helpers.logger import CustomLogger
from helpers.request_sender import RequestSender
from settings import Settings


def get_new_authorization(request_sender: RequestSender, settings: Settings, logger: CustomLogger) -> None:
    access_getter_result = request_sender.get_access_token(
        refresh_token=settings.REFRESH_TOKEN
    )

    if access_getter_result['status_code'] == 200:
        settings.set_new_access_token(access_token=access_getter_result['access_token'])
        logger.log_to_file_and_screen('New access token set')
    elif access_getter_result['status_code'] == 401:
        tokens = request_sender.get_tokens(
            device_id=settings.DEVICE_ID,
            password=settings.PASSWORD,
        )
        if tokens['status_code'] == 200:
            settings.set_new_tokens(
                access_token=tokens['access_token'],
                refresh_token=tokens['refresh_token']
            )
            logger.log_to_file_and_screen('New access and refresh tokens set')
        else:
            raise ConnectionError
