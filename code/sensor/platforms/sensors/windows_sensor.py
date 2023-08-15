from typing import Callable
from abc import ABC, abstractmethod

from sensor.models.data.sensor_datum import SensorDatum
from sensor.platforms.sensors.platform_sensor import PlatformSensor
from models.platform_type import PlatformType


class WindowsSensor(PlatformSensor, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.WINDOWS


    @staticmethod
    def get_initializer_method() -> Callable:
        return WindowsSensor.initialize_sensor_windows


    @staticmethod
    def get_reader_method() -> Callable:
        return WindowsSensor.read_sensor_windows

    ## Methods

    async def initialize_sensor_windows(self):
        return


    @abstractmethod
    async def read_sensor_windows(self) -> list[SensorDatum]:
        pass
