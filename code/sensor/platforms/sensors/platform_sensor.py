from abc import ABC, abstractmethod
from typing import Callable

from models.platform_type import PlatformType


class PlatformSensor(ABC):
    ## Statics

    @staticmethod
    @abstractmethod
    def get_platform_type() -> PlatformType:
        pass


    @staticmethod
    @abstractmethod
    def get_initializer_method() -> Callable:
        pass


    @staticmethod
    @abstractmethod
    def get_reader_method() -> Callable:
        pass
