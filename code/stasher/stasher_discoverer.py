from pathlib import Path

from common.implementation_finder import ImplementationFinder
from stasher.models.storage_adapter import StorageAdapter
from stasher.models.config.storage_config import StorageConfig
from utilities.logging.logging import Logging


## todo: cache discovered storage clients, and inject this service vs instantiate it every time
class StasherDiscoverer:
    ## Lifecycle

    def __init__(self):
        self.logger = Logging.LOGGER
        self.implementation_finder = ImplementationFinder()

    ## Methods

    def discover_stashers(self, stashers_directory_path: Path) -> dict[StorageAdapter, StorageConfig]:
        """
        Discover all available storage clients by looking through the provided storage clients directory, and return a mapping of
        storage clients to their configuration classes. 

        Here's a very simple example of what the storage clients directory might look like:
        storage/
            clients/
                stasher_alpha/
                    stasher_alpha.py
                    stasher_alpha_config.py

        Where individual storage clients have their own subdirectory, with their client and configuration.

        Note that there aren't any hard requirements for the names of the files or directories, but rather that the
        classes themselves inherit from the expected base classes. Some storage client calling itself
        "MySuperCoolStorageClient" will only be discovered as a storage client if it inherits from
        `StorageAdapter`. Similarly, it's associated configuration class would have to inherit from `StorageConfig`.
        """

        stasher_config_map = {}

        stasher_directory: Path
        for stasher_directory in stashers_directory_path.iterdir():
            ## Make sure we're only looking at directories
            if (not stasher_directory.is_dir()):
                continue

            ## Ignore __dunder__ directories like __pycache__
            if (stasher_directory.name.startswith("__") and stasher_directory.name.endswith("__")):
                continue

            ## Look for implementation classes
            stasher_class = self.implementation_finder.find_implementation_class(Path(stasher_directory), base_class=[StorageAdapter])
            storage_configuration_class = self.implementation_finder.find_implementation_class(Path(stasher_directory), base_class=[StorageConfig])

            ## Couldn't find the driver class? No problem, just move on to the next directory
            if (stasher_class is None):
                self.logger.debug(f"Unable to find storage client class in directory: {stasher_directory}")
                continue

            ## Same for the configuration
            if (storage_configuration_class is None):
                self.logger.debug(f"Unable to find storage client configuration class in directory: {stasher_directory}")
                continue

            stasher_config_map[stasher_class] = storage_configuration_class

        return stasher_config_map
