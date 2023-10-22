from abc import ABC, abstractmethod
from typing import List

from sensor.models.data.sensor_datum import SensorDatum


class StorageAdapter(ABC):

    @property
    @abstractmethod
    def storage_type(self) -> str:
        pass


    @abstractmethod
    def store(self, data: List[SensorDatum]):
        pass
