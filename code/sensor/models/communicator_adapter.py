from abc import ABC, abstractmethod

from sensor.models.sensor_type import SensorType


class CommunicatorAdapter(ABC):
    ## Statics

    @staticmethod
    @abstractmethod
    def register_sensor(*args):
        pass


    @staticmethod
    @abstractmethod
    def unregister_sensor(*args):
        pass

    ## Properties

    @property
    @abstractmethod
    def sensor_type(self) -> SensorType:
        pass
