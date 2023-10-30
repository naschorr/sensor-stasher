from abc import ABC, abstractmethod

from sensor.models.sensor_type import SensorType


class CommunicatorAdapter(ABC):

    ## Properties

    @property
    @abstractmethod
    def sensor_type(self) -> SensorType:
        pass
