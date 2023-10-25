from abc import ABC, abstractmethod

from models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.config.sensor_config import SensorConfig


class SensorAdapter(ABC):
    ## Lifecycle

    @abstractmethod
    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, sensor_configuration: SensorConfig):
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
