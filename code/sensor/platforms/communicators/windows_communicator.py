from typing import Callable
from abc import ABC, abstractmethod

from sensor.models.data.sensor_datum import SensorDatum
from sensor.platforms.communicators.platform_communicator import PlatformCommunicator
from models.platform_type import PlatformType


class WindowsCommunicator(PlatformCommunicator, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.WINDOWS

    @staticmethod
    def get_initialization_method() -> Callable:
        return WindowsCommunicator.initialize_communicator_windows

    ## Methods

    @abstractmethod
    def initialize_communicator_windows(self):
        pass
