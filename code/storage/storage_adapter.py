from abc import ABC, abstractmethod
from typing import List

from sensor.sensor_datum import SensorDatum


class StorageAdapter(ABC):
    @abstractmethod
    def store(self, data: List[SensorDatum]):
        pass
