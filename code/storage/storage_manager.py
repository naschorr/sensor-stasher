import pydantic

from common.implementation_instantiator import ImplementationInstantiator
from common.models.config.sensor_stasher_config import SensorStasherConfig
from storage.storage_discoverer import StorageDiscoverer
from storage.models.storage_adapter import StorageAdapter
from sensor.models.data.sensor_datum import SensorDatum
from utilities.logging.logging import Logging

class StorageManager:
    def __init__(
            self,
            logger: Logging,
            configuration: SensorStasherConfig,
            storage_clients_configuration: pydantic.BaseModel,
            storage_discoverer: StorageDiscoverer,
            implementation_instantiator: ImplementationInstantiator
    ):
        self.logger = logger
        self.configuration = configuration
        self.storage_clients_configuration = storage_clients_configuration
        self.system_type = configuration.system_type
        self.system_id = configuration.system_id
        self.storage_discoverer = storage_discoverer
        self.implementation_instantiator = implementation_instantiator

        ## Storage client preparation
        storage_client_config_map = self.storage_discoverer.discover_storage_clients(self.configuration.storage_clients_directory_path)
        self._available_storage_clients: set[StorageAdapter] = set(list(storage_client_config_map.keys()))
        self._registered_storage_clients: set[StorageAdapter] = self.implementation_instantiator.instantiate_classes(
            storage_client_config_map,
            self.storage_clients_configuration
        )

        self.logger.info(f"Initialized {len(self._registered_storage_clients)} of {len(self._available_storage_clients)} storage clients.")

    ## Properties

    @property
    def available_storage_clients(self) -> set[StorageAdapter]:
        return self._available_storage_clients


    @property
    def registered_storage_clients(self) -> set[StorageAdapter]:
        return self._registered_storage_clients

    ## Methods

    def store(self, data: list[SensorDatum]):
        ## Can't store data without a place to store it
        if (not self.registered_storage_clients):
            raise RuntimeError("No storage adapters registered")
        
        ## No data to store? No worries, just skip this iteration
        if (not data):
            return

        for storage_client in self.registered_storage_clients:
            storage_client.store(data)
