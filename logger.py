

class DeviceLogger:
    def log_to_file_and_screen(self, message: str) -> None:
        print(message)

    def log_to_file(self, message: str) -> None:
        pass

    def log_to_screen(self, message: str) -> None:
        print(message)
