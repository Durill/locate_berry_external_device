from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from logger import DeviceLogger
from user_input import UserInput


# TODO: Make method for user input and whole mechanism for CLI
# TODO: Make method for generating device_id if isn't in file

@dataclass
class Settings:
    SERVER_URL: str = "http://127.0.0.1:8000"
    FILE_NAME: str = "device_settings.txt"
    SYSTEMS_CHECK: bool = True
    IS_REGISTERED: bool = False
    DEVICE_ID: str = ""
    DEVICE_NAME: str = ""
    OWNER_EMAIL: str = ""
    TRANSMITTING: bool = True

    def __init__(self, logger: DeviceLogger) -> None:
        self.logger = logger

    def checking_and_setting_device_settings(self) -> None:
        base_dir = Path(__file__).resolve()
        if not Path(base_dir.with_name(self.FILE_NAME)).is_file():
            self.logger.log_to_file_and_screen("First launch, generating settings...")
            self._generate_settings_file()

    def _generate_settings_file(self) -> None:
        self.DEVICE_ID = str(uuid4())
        self.OWNER_EMAIL = UserInput.email_input()
        self.DEVICE_NAME = UserInput.device_name_input()

        with (open(self.FILE_NAME, 'w') as file):
            payload = f"""
            DEVICE_ID={self.DEVICE_ID}
            DEVICE_NAME={self.DEVICE_NAME}
            IS_REGISTERED={self.IS_REGISTERED}
            OWNER_EMAIL={self.OWNER_EMAIL}
            """
            file.write(payload)

    def set_values_from_file(self, file_values: dict) -> None:
        self.DEVICE_ID = file_values['DEVICE_ID']
        self.OWNER_EMAIL = file_values['OWNER_EMAIL']
        self.IS_REGISTERED = True if file_values['IS_REGISTERED'] == 'True' else False

    def set_generated_values(
        self,
        device_id: str,
        owner_email: str,
        is_registered: bool
    ) -> None:
        if not device_id:
            print('\n!!!! DEVICE_ID NOT GENERATED !!!\n')

        if not owner_email:
            print('\n!!!! Owner email NOT SAVED !!!\n')

        if not is_registered:
            print('\n!!!! Device NOT REGISTERED !!!\n')

        self.DEVICE_ID = device_id
        self.OWNER_EMAIL = owner_email
        self.IS_REGISTERED = is_registered

        print('Values set properly')


settings = Settings()
