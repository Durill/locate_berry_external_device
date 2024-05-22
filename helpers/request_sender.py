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
            url="/api/device/register/",
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

    def get_tokens(self, device_id: str, password: str) -> Dict[str, Union[str, int]]:
        payload = {
            "id": device_id,
            "password": password
        }

        result = self._synchronous_request.send_post_request(
            url="/api/token/",
            payload=payload
        )
        body = result.text

        response_parameters = {
            "access_token": body["access"],
            "refresh_token": body["refresh"],
            "status_code": result.status_code
        }

        return response_parameters

    def get_access_token(self, refresh_token: str) -> Dict[str, Union[str, int]]:
        payload = {
            "refresh": refresh_token
        }

        result = self._synchronous_request.send_post_request(
            url="/api/token/refresh/",
            payload=payload
        )
        body = result.text

        response_parameters = {
            "access_token": body["access"],
            "status_code": result.status_code
        }

        return response_parameters

    def create_trip(self, geometry: dict, device_id: str, access_token: str) -> Dict[str, Union[str, int]]:
        payload = {
            "geometry": geometry,
            "device": device_id
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        result = self._synchronous_request.send_post_request(
            url="/api/trip/start/",
            payload=payload,
            headers=headers
        )
        body = result.text

        response_parameters = {
            "trip_id": body["trip_id"],
            "status_code": result.status_code
        }

        return response_parameters

    def update_trip(
        self,
        geometry: dict,
        device_id: str,
        trip_id: str,
        access_token: str
    ) -> Dict[str, Union[str, int]]:
        payload = {
            "geometry": geometry,
            "device": device_id
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        result = self._synchronous_request.send_put_request(
            url=f"/api/trip/{trip_id}/update/",
            payload=payload,
            headers=headers
        )

        response_parameters = {
            "status_code": result.status_code
        }

        return response_parameters
