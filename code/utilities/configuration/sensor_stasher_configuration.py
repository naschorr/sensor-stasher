from pathlib import Path
from typing import Optional

from models.config.sensor_stasher_config import SensorStasherConfig
from utilities.configuration.hierarchical_configuration import HierarchicalConfiguration
from utilities.misc import get_root_path


class SensorStasherConfiguration(HierarchicalConfiguration):

    ## Methods

    def load_configuration(self, directory_path: Optional[Path] = None) -> SensorStasherConfig:
        config = self.build_config_hierarchy(directory_path or get_root_path())

        return SensorStasherConfig(**config)
