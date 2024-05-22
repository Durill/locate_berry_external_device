from typing import Dict, Union

from requests.synchronous import SynchronousRequest
from user_input.handler import UserInputHandler

__all__ = ("RequestSender",)


class RequestSender:
    def __init__(
        self,
        synchronous_request: SynchronousRequest
    ) -> None:
        super().__init__()
        self._synchronous_request = synchronous_request

    def health_check(self) -> int:
        return self._synchronous_request.send_get_request(
            url="/api/health-check/"
        ).status_code

    def register_device(self) -> Dict[str, Union[str, int]]:
        email = UserInputHandler.email_input()
        password = UserInputHandler.password_input()
        payload = {
            "user_email": email,
            "password": password,
        }

        result = self._synchronous_request.send_post_request(
            url="/device/api/register/",
            payload=payload
        )
        body = result.text

        register_parameters = {
            "device_id": body["device_id"],
            "email": email,
            "password": password,
            "status_code": result.status_code
        }

        return register_parameters
