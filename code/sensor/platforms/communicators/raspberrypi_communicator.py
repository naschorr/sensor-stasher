from typing import Callable
from abc import ABC, abstractmethod

from common.models.platform_type import PlatformType
from sensor.platforms.communicators.platform_communicator import PlatformCommunicator


class RaspberryPiCommunicator(PlatformCommunicator, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.RASPBERRYPI

    ## Methods

    @abstractmethod
    def initialize_communicator_raspberrypi(self):
        pass
