from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from logger import CustomLogger
from user_input import UserInput

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

    SYSTEMS_CHECK: bool = True
    IS_REGISTERED: bool = False
    TRANSMITTING: bool = True
    SETTINGS_SETTED: bool = False

    def __init__(self, logger: CustomLogger) -> None:
        self.logger = logger

    def checking_and_setting_device_settings(self) -> None:

        if self.SETTINGS_SETTED:
            return None

        base_dir = Path(__file__).resolve()
        if not Path(base_dir.with_name(self.FILE_NAME)).is_file():
            self.logger.log_to_file_and_screen("First launch, generating settings...")
            self._generate_settings_file()
        else:
            self.logger.log_to_file_and_screen("Reading settings from file...")
            self.set_values_from_file()

        return None

    def _generate_settings_file(self) -> None:
        self.DEVICE_ID = str(uuid4())
        self.OWNER_EMAIL = UserInput.email_input()
        self.DEVICE_NAME = UserInput.device_name_input()

        with (open(self.FILE_NAME, 'w') as file):
            payload = f"DEVICE_ID={self.DEVICE_ID}\nDEVICE_NAME={self.DEVICE_NAME}\nOWNER_EMAIL={self.OWNER_EMAIL}"
            file.write(payload)

        return None

    def set_values_from_file(self) -> None:
        file_dict: dict = {}
        with open(self.FILE_NAME, 'r') as file:
            lines = file.readlines()
            print(lines)
            for line in lines:
                print(line)
                split_list = line.split('=', )
                print(split_list)
                file_dict[split_list[0]] = split_list[1].replace('\n', '')
        self.DEVICE_ID = file_dict['DEVICE_ID']
        self.OWNER_EMAIL = file_dict['OWNER_EMAIL']
        # TODO: this shit don't work nigga -> KeyError: 'IS_REGISTERED'
        self.IS_REGISTERED = (
            True
            if file_dict['IS_REGISTERED'] and file_dict['IS_REGISTERED'] == 'True'
            else False
        )

        return None

    def add_is_registered_to_file(self) -> None:
        with open(self.FILE_NAME, 'a') as file:
            file.write(f"IS_REGISTERED={True}")
