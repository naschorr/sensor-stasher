from abc import ABC, abstractmethod

from ..platform_base import PlatformBase
from sensor.models.data.sensor_measurement import SensorMeasurement


class PlatformSensor(PlatformBase, ABC):

    ## Methods

    @abstractmethod
    async def read() -> list[SensorMeasurement]:
        pass
