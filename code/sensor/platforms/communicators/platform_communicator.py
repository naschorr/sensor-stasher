from typing import Callable
from abc import ABC, abstractmethod

from models.platform_type import PlatformType


class PlatformCommunicator(ABC):
    ## Statics

    @staticmethod
    @abstractmethod
    def get_platform_type() -> PlatformType:
        pass


    @staticmethod
    @abstractmethod
    def get_initializer_method() -> Callable:
        pass
