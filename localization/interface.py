from abc import ABC, abstractmethod

__all__ = ("ILocalization",)


class ILocalization(ABC):

    @abstractmethod
    def set_and_power_module(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_actual_localization(self):
        raise NotImplementedError
