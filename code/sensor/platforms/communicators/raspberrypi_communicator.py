from typing import Callable
from abc import ABC, abstractmethod

from sensor.models.data.sensor_datum import SensorDatum
from sensor.platforms.communicators.platform_communicator import PlatformCommunicator
from models.platform_type import PlatformType


class RaspberryPiCommunicator(PlatformCommunicator, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.RASPBERRYPI

    @staticmethod
    def get_initialization_method() -> Callable:
        return RaspberryPiCommunicator.initialize_communicator_raspberrypi

    ## Methods

    @abstractmethod
    def initialize_communicator_raspberrypi(self):
        pass
