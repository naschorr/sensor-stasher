from pathlib import Path
import pydantic

from sensor.sensor_discoverer import SensorDiscoverer
from sensor.models.config.sensor_config import SensorConfig
from sensor.models.sensor_adapter import SensorAdapter
from utilities.configuration.hierarchical_configuration import HierarchicalConfiguration
from utilities.misc import get_root_path


class DynamicSensorConfiguration(HierarchicalConfiguration):
    ## Lifecycle

    def __init__(self, sensor_discoverer: SensorDiscoverer):
        self.sensor_discoverer = sensor_discoverer


    ## Methods

    def _build_pydantic_config_model_args_for_sensors(self, sensor_config_map: dict[SensorAdapter, SensorConfig]) -> dict:
        """
        Maps the sensor (by it's self assigned name, or failing that it's module name) to a tuple of type:
        (SensorConfig, None).
        """

        output = {}
        for driver, config in sensor_config_map.items():
            ## Really lazy, but it works as long as new sensors are added that follow existing naming conventions.
            name = driver.__module__.split("_driver")[0]

            ## Pydantic expects a name to map to a tuple of (type, default)
            output[name.lower()] = (config, {})

        return output


    def _build_sensors_configuration_model(self, sensors_directory_path: Path) -> type[pydantic.BaseModel]:
        """
        Builds a pydantic model to store configuration options for platform specific sensors.
        """

        sensor_config_map = self.sensor_discoverer.discover_sensors(sensors_directory_path)

        return pydantic.create_model(
            "DynamicSensorConfiguration",
            **self._build_pydantic_config_model_args_for_sensors(sensor_config_map)
        )


    def load_sensors_configuration(self, config_directory_path: Path, sensors_directory_path: Path) -> pydantic.BaseModel:
        """
        Loads the configuration file from the provided directory (or the app's root if not provided) and returns a
        validated SensorStasherConfig object.

        :param sensors_directory_path: Optional path to load configuration files from. If None, then the program's root (cwd/..) will be searched.
        :type sensors_directory_path: Path, optional
        :return: SensorStasherConfig object containing the validated configuration data.
        :rtype: SensorStasherConfig
        """

        config = self.build_config_hierarchy(config_directory_path)
        model = self._build_sensors_configuration_model(sensors_directory_path)

        return model(**config)
