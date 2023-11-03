from pathlib import Path
from typing import Optional

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.sensor_discoverer import SensorDiscoverer
from stasher.stasher_discoverer import StasherDiscoverer
from utilities.configuration.sensor_stasher_configuration import SensorStasherConfiguration
from utilities.configuration.dynamic_sensor_configuration import DynamicSensorConfiguration
from utilities.configuration.dynamic_stasher_configuration import DynamicStasherConfiguration
from utilities.misc import get_root_path


class Configuration:

    ## Lifecycle

    def __init__(
            self,
            sensor_discoverer: SensorDiscoverer,
            stasher_discoverer: StasherDiscoverer,
            config_directory_path: Optional[Path] = None,
            sensors_directory_path: Optional[Path] = None,
            stashers_directory_path: Optional[Path] = None
    ):
        self._config_directory_path = config_directory_path or get_root_path()
        self._sensor_stasher_config_loader = SensorStasherConfiguration()
        self._sensor_stasher_config = None

        self._sensors_directory_path = sensors_directory_path or self.sensor_stasher_configuration.sensors_directory_path
        self._sensors_config_loader = DynamicSensorConfiguration(sensor_discoverer)
        self._sensors_config = None

        self._stashers_directory_path = stashers_directory_path or self.sensor_stasher_configuration.stashers_directory_path
        self._stashers_config_loader = DynamicStasherConfiguration(stasher_discoverer)
        self._stashers_config = None

    ## Properties

    @property
    def sensor_stasher_configuration(self) -> SensorStasherConfig:
        if (self._sensor_stasher_config is None):
            self._sensor_stasher_config = self._load_configuration()

        return self._sensor_stasher_config

    @property
    def sensors_configuration(self):
        if (self._sensors_config is None):
            self._sensors_config = self._load_sensors_configuration()

        return self._sensors_config

    @property
    def stasher_configuration(self):
        if (self._stashers_config is None):
            self._stashers_config = self._load_stashers_configuration()

        return self._stashers_config

    ## Methods

    def _load_configuration(self) -> SensorStasherConfig:
        return self._sensor_stasher_config_loader.load_configuration(self._config_directory_path)


    ## Separate sensors config loader to avoid polluting the load_configuration return type with some runtime generated shenanigans
    def _load_sensors_configuration(self):
        return self._sensors_config_loader.load_sensors_configuration(self._config_directory_path, self._sensors_directory_path)


    ## Separate storage clients config loader to avoid polluting the load_configuration return type with some runtime generated shenanigans
    def _load_stashers_configuration(self):
        return self._stashers_config_loader.load_stashers_configuration(self._config_directory_path, self._stashers_directory_path)
