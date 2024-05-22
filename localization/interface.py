from abc import ABC, abstractmethod
from typing import Optional

__all__ = ("ILocalization",)

from localization import LocalizationPoint


class ILocalization(ABC):

    @abstractmethod
    def set_and_power_module(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_actual_localization(self) -> Optional[LocalizationPoint]:
        raise NotImplementedError
