from abc import ABC, abstractmethod


class IRequest(ABC):
    @abstractmethod
    def send_get_request(self, url: str):
        raise NotImplementedError

    @abstractmethod
    def send_post_request(self, url: str, payload: dict = None):
        raise NotImplementedError
