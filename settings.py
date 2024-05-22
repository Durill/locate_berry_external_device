from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from helpers.logger import CustomLogger
from user_input.handler import UserInputHandler

__all__ = ("Settings",)


# TODO: Make method for user input and whole mechanism for CLI
# TODO: Make method for generating device_id if isn't in file

@dataclass
class Settings:
    SERVER_URL: str = "http://127.0.0.1:8000"
    FILE_NAME: str = "device_settings.txt"

    DEVICE_ID: str = ""
    DEVICE_NAME: str = ""
    OWNER_EMAIL: str = ""
    PASSWORD: str = ""

    ACCESS_TOKEN: str = ""
    REFRESH_TOKEN: str = ""

    SYSTEM_CHECKED: bool = False
    IS_REGISTERED: bool = False
    TRANSMITTING: bool = True
    SETTINGS_SET: bool = False

    def __init__(self, logger: CustomLogger) -> None:
        self.logger = logger

    def checking_device_settings(self) -> bool:
        base_dir = Path(__file__).resolve()
        return True if Path(base_dir.with_name(self.FILE_NAME)).is_file() else False

    def set_values_from_file(self) -> None:
        file_dict: dict = {}
        with open(self.FILE_NAME, 'r') as file:
            lines = file.readlines()
            for line in lines:
                split_list = line.split('=', )
                file_dict[split_list[0]] = split_list[1].replace('\n', '')
        self.DEVICE_ID = file_dict['DEVICE_ID']
        self.OWNER_EMAIL = file_dict['OWNER_EMAIL']
        self.PASSWORD = file_dict['PASSWORD']
        self.IS_REGISTERED = (
            True
            if 'IS_REGISTERED' in file_dict and file_dict['IS_REGISTERED'] == 'True'
            else False
        )
        self.SETTINGS_SET = True

        return None

    def register_and_bind_device(self, register_parameters: dict):
        if register_parameters['status_code'] == 201:
            self.DEVICE_ID = register_parameters['device_id']
            self.OWNER_EMAIL = register_parameters['email']
            self.PASSWORD = register_parameters['password']
            self.IS_REGISTERED = True

            with (open(self.FILE_NAME, 'w') as file):
                payload = f"DEVICE_ID={self.DEVICE_ID}\nDEVICE_NAME={self.DEVICE_NAME}\nOWNER_EMAIL={self.OWNER_EMAIL}\nIS_REGISTERED={self.IS_REGISTERED}"
                file.write(payload)
        else:
            self.logger.log_to_file_and_screen(
                f"Registering operation failed, status code: {register_parameters['status_code']}"
            )
