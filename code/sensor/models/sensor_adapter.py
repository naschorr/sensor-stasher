from abc import ABC, abstractmethod
from typing import Optional

from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.config.sensor_config import SensorConfig


class SensorAdapter(ABC):
    @abstractmethod
    def __init__(self, configuration: SensorConfig):
        pass

    ## Properties

    @property
    @abstractmethod
    def sensor_name(self) -> str:
        pass


    @property
    @abstractmethod
    def sensor_id(self) -> str:
        pass

    ## Methods

    @abstractmethod
    async def read(self) -> list[SensorDatum]:
        pass
