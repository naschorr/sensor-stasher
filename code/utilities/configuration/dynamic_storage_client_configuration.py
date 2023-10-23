from pathlib import Path
import pydantic

from storage.storage_discoverer import StorageDiscoverer
from storage.models.storage_adapter import StorageAdapter
from storage.models.config.storage_config import StorageConfig
from utilities.configuration.hierarchical_configuration import HierarchicalConfiguration
from utilities.misc import get_root_path


class DynamicStorageClientConfiguration(HierarchicalConfiguration):
    ## Lifecycle

    def __init__(self, storage_discoverer: StorageDiscoverer):
        self.storage_discoverer = storage_discoverer

    ## Methods

    def _build_pydantic_config_model_args_for_storage_clients(self, storage_client_config_map: dict[StorageAdapter, StorageConfig]) -> dict:
        """
        Maps the storage client (by it's self assigned name, or failing that it's module name) to a tuple of type:
        (StorageConfig, None).
        """

        output = {}
        for driver, config in storage_client_config_map.items():
            ## Really lazy, but it works as long as new storage_clients are added that follow existing naming conventions.
            ## todo: improve this!
            name = driver.__module__.split("_client")[0]
            if (hasattr(config, "sensor_name")):
                name = config.sensor_name

            ## Pydantic expects a name to map to a tuple of (type, default)
            output[name.lower()] = (config, None)

        return output


    def _build_storage_clients_configuration_model(self, storage_clients_directory_path: Path) -> type[pydantic.BaseModel]:
        """
        Builds a pydantic model to store configuration options for platform specific storage_clients.
        """

        storage_client_config_map = self.storage_discoverer.discover_storage_clients(storage_clients_directory_path)

        return pydantic.create_model(
            "DynamicStorageClientConfiguration",
            **self._build_pydantic_config_model_args_for_storage_clients(storage_client_config_map)
        )


    def load_storage_clients_configuration(self, config_directory_path: Path, storage_clients_directory_path: Path) -> pydantic.BaseModel:
        """
        Loads the configuration file from the provided directory (or the app's root if not provided) and returns a
        validated storage_clientstasherConfig object.

        :param storage_clients_directory_path: Optional path to load configuration files from. If None, then the program's root (cwd/..) will be searched.
        :type storage_clients_directory_path: Path, optional
        :return: storage_clientstasherConfig object containing the validated configuration data.
        :rtype: storage_clientstasherConfig
        """

        config = self.build_config_hierarchy(config_directory_path)
        model = self._build_storage_clients_configuration_model(storage_clients_directory_path)

        return model(**config)
