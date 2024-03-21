from httpx import Client


class SynchronousRequests:
    def __init__(self, server_url: str, client: Client) -> None:
        self.server_url = server_url
        self.client = client

    def perform_health_check(self) -> int:
        return self.client.get(
            f"{self.server_url}/api/health-check/"
        ).status_code

    def register_device(
        self,
        device_id: str,
        device_name: str,
        owner_email: str,
    ) -> int:
        payload = {
            "device_id": device_id,
            "device_name": device_name,
            "user_email": owner_email,
        }

        return self.client.post(
            url=f"{self.server_url}/device/api/register/",
            data=payload,
        ).status_code
