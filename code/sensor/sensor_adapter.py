from abc import ABC, abstractmethod
from typing import List

from sensor.models.sensor_datum import SensorDatum


class SensorAdapter(ABC):
    @abstractmethod
    def __init__(self, sensor_id: str):
        pass

    ## Properties

    @property
    @abstractmethod
    def sensor_type(self) -> str:
        pass


    @property
    @abstractmethod
    def sensor_id(self) -> str:
        pass

    ## Methods

    @abstractmethod
    async def read(self) -> List[SensorDatum]:
        pass
