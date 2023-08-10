from abc import ABC, abstractmethod
from typing import List

from sensor.models.data.sensor_datum import SensorDatum
from storage.models.storage_type import StorageType


class StorageAdapter(ABC):

    @property
    @abstractmethod
    def storage_type(self) -> StorageType:
        pass


    @abstractmethod
    def store(self, data: List[SensorDatum]):
        pass
