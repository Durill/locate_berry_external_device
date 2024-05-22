from typing import Dict

from httpx import Client
from requests.interface import IRequest

__all__ = ("SynchronousRequest",)


class SynchronousRequest(IRequest):
    def __init__(self, server_url: str, client: Client) -> None:
        self.server_url = server_url
        self.client = client

    def send_get_request(self, url: str):
        return self.client.get(
            f"{self.server_url}{url}"
        )

    def send_post_request(self, url: str, payload: dict = None, headers: Dict[str, str] = None):
        self.client.post(
            url=f"{self.server_url}{url}",
            data=payload,
            headers=headers,
        )

    def send_put_request(self, url: str, payload: dict = None, headers: Dict[str, str] = None):
        self.client.put(
            url=f"{self.server_url}{url}",
            data=payload,
            headers=headers,
        )
