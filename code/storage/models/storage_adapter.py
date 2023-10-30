from abc import ABC, abstractmethod

from common.models.config.sensor_stasher_config import SensorStasherConfig
from storage.models.config.storage_config import StorageConfig
from storage.models.storage_type import StorageType
from sensor.models.data.sensor_measurement import SensorMeasurement


class StorageAdapter(ABC):
    ## Lifecycle

    @abstractmethod
    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, storage_client_configuration: StorageConfig):
        pass

    ## Properties

    @property
    @abstractmethod
    def storage_type(self) -> StorageType:
        pass

    ## Methods

    @abstractmethod
    def store(self, data: list[SensorMeasurement]):
        pass
