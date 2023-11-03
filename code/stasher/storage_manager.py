import pydantic

from common.implementation_instantiator import ImplementationInstantiator
from common.models.config.sensor_stasher_config import SensorStasherConfig
from stasher.stasher_discoverer import StasherDiscoverer
from stasher.models.storage_adapter import StorageAdapter
from sensor.models.data.sensor_measurement import SensorMeasurement
from utilities.logging.logging import Logging

class StorageManager:
    def __init__(
            self,
            logger: Logging,
            configuration: SensorStasherConfig,
            stashers_configuration: pydantic.BaseModel,
            stasher_discoverer: StasherDiscoverer,
            implementation_instantiator: ImplementationInstantiator
    ):
        self.logger = logger
        self.configuration = configuration
        self.stashers_configuration = stashers_configuration
        self.system_type = configuration.system_type
        self.system_id = configuration.system_id
        self.stasher_discoverer = stasher_discoverer
        self.implementation_instantiator = implementation_instantiator

        ## Storage client preparation
        stasher_config_map = self.stasher_discoverer.discover_stashers(self.configuration.stashers_directory_path)
        self._available_stashers: set[StorageAdapter] = set(list(stasher_config_map.keys()))
        self._registered_stashers: set[StorageAdapter] = self.implementation_instantiator.instantiate_classes(
            stasher_config_map,
            self.stashers_configuration
        )

        self.logger.info(f"Initialized {len(self._registered_stashers)} of {len(self._available_stashers)} storage clients.")

    ## Properties

    @property
    def available_stashers(self) -> set[StorageAdapter]:
        return self._available_stashers


    @property
    def registered_stashers(self) -> set[StorageAdapter]:
        return self._registered_stashers

    ## Methods

    def store(self, data: list[SensorMeasurement]):
        ## Can't store data without a place to store it
        if (not self.registered_stashers):
            raise RuntimeError("No storage adapters registered")
        
        ## No data to store? No worries, just skip this iteration
        if (not data):
            return

        for stasher in self.registered_stashers:
            stasher.store(data)
