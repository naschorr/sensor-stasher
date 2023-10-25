import logging
from pathlib import Path

from common.implementation_finder import ImplementationFinder
from storage.models.storage_adapter import StorageAdapter
from storage.models.config.storage_config import StorageConfig
from utilities.logging.logging import Logging


## todo: cache discovered storage clients, and inject this service vs instantiate it every time
class StorageDiscoverer:
    ## Lifecycle

    def __init__(self):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))
        self.implementation_finder = ImplementationFinder()

    ## Methods

    def discover_storage_clients(self, storage_clients_directory_path: Path) -> dict[StorageAdapter, StorageConfig]:
        """
        Discover all available storage clients by looking through the provided storage clients directory, and return a mapping of
        storage clients to their configuration classes. 

        Here's a very simple example of what the storage clients directory might look like:
        storage/
            clients/
                storage_client_alpha/
                    storage_client_alpha.py
                    storage_client_alpha_config.py

        Where individual storage clients have their own subdirectory, with their client and configuration.

        Note that there aren't any hard requirements for the names of the files or directories, but rather that the
        classes themselves inherit from the expected base classes. Some storage client calling itself
        "MySuperCoolStorageClient" will only be discovered as a storage client if it inherits from
        `StorageAdapter`. Similarly, it's associated configuration class would have to inherit from `StorageConfig`.
        """

        storage_client_config_map = {}

        storage_client_directory: Path
        for storage_client_directory in storage_clients_directory_path.iterdir():
            ## Make sure we're only looking at directories
            if (not storage_client_directory.is_dir()):
                continue

            ## Ignore __dunder__ directories like __pycache__
            if (storage_client_directory.name.startswith("__") and storage_client_directory.name.endswith("__")):
                continue

            ## Look for implementation classes
            storage_client_class = self.implementation_finder.find_implementation_class(Path(storage_client_directory), base_class=[StorageAdapter])
            storage_configuration_class = self.implementation_finder.find_implementation_class(Path(storage_client_directory), base_class=[StorageConfig])

            ## Couldn't find the driver class? No problem, just move on to the next directory
            if (storage_client_class is None):
                self.logger.debug(f"Unable to find storage client class in directory: {storage_client_directory}")
                continue

            ## Same for the configuration
            if (storage_configuration_class is None):
                self.logger.debug(f"Unable to find storage client configuration class in directory: {storage_client_directory}")
                continue

            storage_client_config_map[storage_client_class] = storage_configuration_class

        return storage_client_config_map
