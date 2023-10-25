from typing import Callable
from abc import ABC, abstractmethod

from common.models.platform_type import PlatformType
from sensor.models.data.sensor_datum import SensorDatum
from sensor.platforms.communicators.platform_communicator import PlatformCommunicator


class RaspberryPiCommunicator(PlatformCommunicator, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.RASPBERRYPI

    @staticmethod
    def get_initializer_method() -> Callable:
        return RaspberryPiCommunicator.initialize_communicator_raspberrypi

    ## Methods

    @abstractmethod
    def initialize_communicator_raspberrypi(self):
        pass
