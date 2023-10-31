from pathlib import Path
import pydantic

from common.models.config.sensor_stasher_config import SensorStasherConfig
from stasher.stasher_discoverer import StasherDiscoverer
from stasher.models.storage_adapter import StorageAdapter
from stasher.models.config.storage_config import StorageConfig
from utilities.configuration.hierarchical_configuration import HierarchicalConfiguration


class DynamicStasherConfiguration(HierarchicalConfiguration):
    ## Lifecycle

    def __init__(self, stasher_discoverer: StasherDiscoverer):
        self.stasher_discoverer = stasher_discoverer

    ## Methods

    def _build_pydantic_config_model_args_for_stashers(self, stasher_config_map: dict[StorageAdapter, StorageConfig]) -> dict:
        """
        Maps the storage client (by it's self assigned name, or failing that it's module name) to a tuple of type:
        (StorageConfig, None).
        """

        output = {}
        for driver, config in stasher_config_map.items():
            ## Really lazy, but it works as long as new stashers are added that follow existing naming conventions.
            name = driver.__module__.split("_client")[0]

            ## Pydantic expects a name to map to a tuple of (type, default)
            output[name.lower()] = (config, {})

        return output


    def _build_stashers_configuration_model(self, stashers_directory_path: Path) -> type[pydantic.BaseModel]:
        """
        Builds a pydantic model to store configuration options for platform specific stashers.
        """

        stasher_config_map = self.stasher_discoverer.discover_stashers(stashers_directory_path)

        return pydantic.create_model(
            "DynamicStasherConfiguration",
            **self._build_pydantic_config_model_args_for_stashers(stasher_config_map)
        )


    def load_stashers_configuration(self, config_directory_path: Path, stashers_directory_path: Path) -> pydantic.BaseModel:
        """
        Loads the configuration file from the provided directory (or the app's root if not provided) and returns a
        validated stasherstasherConfig object.

        :param stashers_directory_path: Optional path to load configuration files from. If None, then the program's root (cwd/..) will be searched.
        :type stashers_directory_path: Path, optional
        :return: stasherstasherConfig object containing the validated configuration data.
        :rtype: stasherstasherConfig
        """

        config = self.build_config_hierarchy(config_directory_path)
        model = self._build_stashers_configuration_model(stashers_directory_path)

        return model(**config)
