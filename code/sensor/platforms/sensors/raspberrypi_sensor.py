from typing import Callable
from abc import ABC, abstractmethod

from sensor.models.data.sensor_datum import SensorDatum
from sensor.platforms.sensors.platform_sensor import PlatformSensor
from models.platform_type import PlatformType


class RaspberryPiSensor(PlatformSensor, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.RASPBERRYPI


    @staticmethod
    def get_initializer_method() -> Callable:
        return RaspberryPiSensor.initialize_sensor_raspberrypi


    @staticmethod
    def get_reader_method() -> Callable:
        return RaspberryPiSensor.read_sensor_raspberrypi

    ## Methods

    async def initialize_sensor_raspberrypi(self):
        return


    @abstractmethod
    async def read_sensor_raspberrypi(self) -> list[SensorDatum]:
        pass
