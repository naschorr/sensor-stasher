from typing import Callable
from abc import ABC, abstractmethod

from common.models.platform_type import PlatformType
from sensor.platforms.communicators.platform_communicator import PlatformCommunicator


class WindowsCommunicator(PlatformCommunicator, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.WINDOWS

    ## Methods

    @abstractmethod
    def initialize_communicator_windows(self):
        pass
