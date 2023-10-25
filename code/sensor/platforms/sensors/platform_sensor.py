from abc import ABC, abstractmethod

from ..platform_base import PlatformBase
from sensor.models.data.sensor_datum import SensorDatum


class PlatformSensor(PlatformBase, ABC):

    ## Methods

    @abstractmethod
    async def read() -> list[SensorDatum]:
        pass
