from typing import Callable
from abc import ABC, abstractmethod

from ..platform_base import PlatformBase


class PlatformCommunicator(PlatformBase, ABC):

    ## Statics

    @staticmethod
    @abstractmethod
    def get_initializer_method() -> Callable:
        pass
