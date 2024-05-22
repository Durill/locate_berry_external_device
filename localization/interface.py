from abc import ABC, abstractmethod
from typing import Optional

from shapely import Point

__all__ = ("ILocalization",)


class ILocalization(ABC):

    @abstractmethod
    def set_and_power_module(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_actual_localization(self) -> Optional[Point]:
        raise NotImplementedError
