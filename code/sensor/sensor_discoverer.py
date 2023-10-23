import logging
import os
from pathlib import Path

from common.implementation_finder import ImplementationFinder
from sensor.models.sensor_adapter import SensorAdapter
from sensor.models.config.sensor_config import SensorConfig
from sensor.platforms.platform_manager import PlatformManager
from sensor.platforms.sensors.platform_sensor import PlatformSensor
from sensor.platforms.configurations.platform_config import PlatformConfig
from utilities.misc import get_current_platform
from utilities.logging.logging import Logging


## todo: cache discovered sensors, and inject this service vs instantiate it every time
class SensorDiscoverer:
    ## Lifecycle

    def __init__(self):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))
        self.implementation_finder = ImplementationFinder()

    ## Methods

    def _get_supported_platform_sensor(self) -> type[PlatformSensor]:
        current_platform = get_current_platform()
        return PlatformManager.get_platform_sensor(current_platform)


    def _get_supported_platform_config(self) -> type[PlatformConfig]:
        current_platform = get_current_platform()
        return PlatformManager.get_platform_config(current_platform)


    def discover_sensors(self, sensors_directory_path: Path) -> dict[SensorAdapter, SensorConfig]:
        """
        Discover all available sensors by looking through the provided sensors directory, and return a mapping of
        platform specific sensor drivers to their configuration classes. In this case, "platform specific" refers to
        logic that's only relevant to the platform running the code. A sensor designed to use the GPIO pins on a
        Raspberry Pi doesn't really have an analog on a normal Windows based machine. If a sensor doesn't expose a
        driver for your current platform, then no worries, the sensor simply will simply be ignored.

        Here's a very simple example of what the sensors directory might look like:
        sensors/
            sensor_alpha/
                windows/
                    sensor_alpha_driver_windows.py
                    sensor_alpha_config_windows.py
                sensor_alpha_driver.py
                sensor_alpha_config.py
                sensor_alpha_datum.py

        Where individual sensors have their own subdirectory, base classes, and platform specific implementations:
        - Generic base class that contains platform independent common logic in the `sensor_alpha_driver.py` file and inherit from `SensorAdapter`
        - Generic base class that contains platform independent configuration in `sensor_alpha_config.py` which inherits from `SensorConfig`
        - Sensor specific datum implementation, that will be returned regardless of the platform, which inherits from `SensorDatum`
        - Platform specific subdirectories (ex: `windows`), that contain platform specific implementations of the driver and configuration classes
            - Platform specific driver class that inherits from the generic driver class and that platform specific sensor `WindowsSensor`
            - Platform specific configuration class that inherits from the generic configuration class and that platform specific sensor `WindowsSensor`

        Note that there aren't any hard requirements for the names of the files or directories, but rather that the
        classes themselves inherit from the expected base classes. Some sensor driver calling itself
        "MySuperCoolSensorDriverForWindows" will only be discovered as a sensor driver if it inherits from
        `SensorAdapter` somewhere, and `WindowsSensor`. It's associated configuration class would have to inherit from 
        `SensorConfig` and `WindowsConfig`.
        """

        sensor_config_map = {}
        supported_platform_sensor = self._get_supported_platform_sensor()
        supported_platform_config = self._get_supported_platform_config()

        sensor_directory: Path
        for sensor_directory in sensors_directory_path.iterdir():
            ## Make sure we're only looking at directories
            if (not sensor_directory.is_dir()):
                continue

            ## Ignore __dunder__ directories like __pycache__
            if (sensor_directory.name.startswith("__") and sensor_directory.name.endswith("__")):
                continue

            ## Get the files and directories in the current sensor directory
            directory_path: str
            platform_directories: list[str]
            directory_path, platform_directories, _ = next(os.walk(sensor_directory)) # type: ignore

            ## Look for root level implementation classes
            root_driver_class = self.implementation_finder.find_implementation_class(Path(directory_path), base_class=[SensorAdapter])
            root_configuration_class = self.implementation_finder.find_implementation_class(Path(directory_path), base_class=[SensorConfig])

            ## Couldn't find the driver class? No problem, just move on to the next directory
            if (root_driver_class is None):
                self.logger.debug(f"Unable to find driver class in directory: {sensor_directory}")
                continue

            ## Look for platform specific implementation classes
            platform_driver_class = None
            platform_configuration_class = None
            for platform_directory in [Path(directory_path) / platform_directory for platform_directory in platform_directories]:
                ## todo: This should really check for root_driver_class instead of the more generic SensorAdapter, but
                ## I've noticed issues where the builtin issubclass function doesn't correctly identify if the sub class
                ## inherits from the base class. However it works as expected if I manually resolve the
                ## root_driver_class. Weird.
                platform_driver_class = self.implementation_finder.find_implementation_class(
                    platform_directory,
                    base_class=[SensorAdapter, supported_platform_sensor]
                )

                if (platform_driver_class is not None and root_configuration_class is not None):
                    platform_configuration_class = self.implementation_finder.find_implementation_class(
                        platform_directory,
                        base_class=[SensorConfig, supported_platform_config]
                    )
                    break

            ## Did we find a platform specific driver class?
            if (platform_driver_class is None):
                self.logger.warn(f"Unable to find platform specific driver class in directory: {sensor_directory}")
                continue

            ## Get the most specific configuration class, and persist the driver -> configuration mapping
            configuration_class = platform_configuration_class if (platform_configuration_class is not None) else root_configuration_class
            sensor_config_map[platform_driver_class] = configuration_class

        return sensor_config_map
