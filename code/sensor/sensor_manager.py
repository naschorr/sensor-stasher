import logging
import inspect
import importlib
import sys
import contextlib
from typing import Optional
from pathlib import Path

from sensor.models.sensor_adapter import SensorAdapter
from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.config.sensor_config import SensorConfig
from sensor.exceptions.sensor_init_exception import SensorInitException
from utilities.configuration import Configuration
from utilities.logging.logging import Logging


class SensorManager:
    ## Lifecycle

    def __init__(self):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        ## Configuration
        configuration = Configuration.load_configuration()
        assert (configuration is not None)
        sensors_directory_path = configuration.sensors_directory_path


        ## Sensor preparation
        sensor_and_config_data = self._discover_sensors(sensors_directory_path)
        self._available_sensors: set[SensorAdapter] = {sensor for sensor, _ in sensor_and_config_data}
        self._registered_sensors: set[SensorAdapter] = self._initialize_sensors(sensor_and_config_data)

        self.logger.info(f"Initialized {len(self._registered_sensors)} of {len(self._available_sensors)} sensors.")

    ## Properties

    @property
    def available_sensors(self) -> set[SensorAdapter]:
        return self._available_sensors


    @property
    def registered_sensors(self) -> set[SensorAdapter]:
        return self._registered_sensors

    ## Methods

    def _discover_sensors(self, sensors_directory_path: Path) -> set[tuple[SensorAdapter, SensorConfig]]:
        """
        Discover all available sensors by traversing the sensors directory, and looking for driver classes (that inherit
        from the base SensorAdapter class) and configuration classes (that inherit from the base SensorConfig class).
        Pair up a corresponding driver and configuration class, and save them for future initialization.
        """

        sensor_and_config_data = set()

        sensor_directory: Path
        for sensor_directory in sensors_directory_path.iterdir():
            ## Make sure we're only looking at directories
            if (not sensor_directory.is_dir()):
                continue

            driver_class = None
            configuration_class = None

            ## Look at the .py files in the sensor_directory and determine if they are sensors (i.e. they inherit from
            ## SensorAdapter). Kudos to https://stackoverflow.com/a/55067404 for the slick class check
            sensor_file: Path
            for sensor_file in sensor_directory.iterdir():
                if (sensor_file.suffix != ".py"):
                    continue

                ## Tentative import
                sys.path.append(str(sensor_directory))
                candidate_module = importlib.import_module(sensor_file.stem)

                cls_found = False
                for _, cls in inspect.getmembers(candidate_module, inspect.isclass):
                    ## Find the driver class
                    if (issubclass(cls, SensorAdapter) and cls is not SensorAdapter and cls.__module__ == candidate_module.__name__):
                        driver_class = cls
                        cls_found = True
                        break
                    ## Find the configuration class
                    elif (issubclass(cls, SensorConfig) and cls is not SensorConfig and cls.__module__ == candidate_module.__name__):
                        configuration_class = cls
                        cls_found = True
                        break

                ## Clean up the module if it's not what we're looking for and start over with the next file
                if (not cls_found):
                    del candidate_module
                    sys.path.remove(str(sensor_directory))
                    continue

            ## Couldn't find the driver class? No problem, just move on to the next directory
            if (driver_class is None):
                continue

            sensor_and_config_data.add((driver_class, configuration_class))

        return sensor_and_config_data


    def _sensor_configuration_retriever(self, sensor_config: SensorConfig) -> Optional[SensorConfig]:
        """
        Attempts to find a configuration property with the same type as the provided sensor configuration class.
        For example: the PMS7003Config sensor config would yield the pms7003 property of the Configuration class.
        """

        configuration = Configuration.load_configuration()

        for _, cls in inspect.getmembers(configuration):
            with contextlib.suppress(TypeError):
                ## todo: Improve this. `isinstance` wasn't really playing nice for the following:
                ## sensor_config: <class 'ds18b20_config.DS18B20Config'> and
                ## cls: DS18B20Config(...). I'm sure it's something simple though
                if (
                        hasattr(cls, "__module__") and
                        cls.__module__ is not None and
                        cls.__module__.endswith(sensor_config.__module__)
                ):
                    return cls

        return None


    def _instantiate_sensor_driver(self, driver_class: SensorAdapter, configuration_class: Optional[SensorConfig]) -> SensorAdapter:
        """
        Handles instantiating the sensor driver from a given driver class and configuration class. Also attempts to
        gracefully handle missing configuration classes.
        """

        ## If we found a configuration class, use that to find the actual processed configuration class of the same type
        configuration = None
        if (configuration_class is not None):
            configuration = self._sensor_configuration_retriever(configuration_class)

        ## Extract the parameters used to instantiate the driver class
        parameters = [parameter for name, parameter in inspect.signature(driver_class.__init__).parameters.items()]

        ## Less than two parameters? It can't have a `configuration` parameter.
        if (len(parameters) < 2):
            return driver_class()
        ## What if it does (potentially) have the expected parameters?
        elif (len(parameters) == 2):
            ## Determine if the driver class requires configuration, and instantiate it
            if (configuration is not None):
                return driver_class(configuration)
            elif (configuration is None and parameters[1].annotation is Optional):
                return driver_class()
            else:
                raise SensorInitException(f"No configuration file provided with a non-optional configuration parameter for sensor: {driver_class.sensor_name}")
        ## Otherwise, something's gone wrong
        else:
            raise SensorInitException(f"Invalid number of parameters for sensor: {driver_class.sensor_name}")


    def _initialize_sensors(self, sensor_and_config_data: set[tuple[SensorAdapter, SensorConfig]]) -> set[SensorAdapter]:
        """
        Initialize the available sensors, and inject the relevant configuration property into them (if it exists). Note
        that issues with sensor initialization won't stop the rest from initializing.
        """

        sensors = set()

        for driver_class, configuration_class in sensor_and_config_data:
            try:
                sensors.add(self._instantiate_sensor_driver(driver_class, configuration_class))
            except Exception as e:
                ## Couldn't instantiate? No worries, just ignore it and move on
                self.logger.warn(f"Unable to instantiate sensor '{driver_class}'", exc_info=e)
                continue

        return sensors


    async def accumulate_all_sensor_data(self) -> list[SensorDatum]:
        """
        Look through all registered sensors and read their data. Returns a list of all the sensor data that was read.
        """

        sensor_data = []

        for sensor in self.registered_sensors:
            data = None
            try:
                data = await sensor.read()
            except Exception as e:
                ## Don't let a single failed sensor read stop the rest
                self.logger.exception(f"Unable to read from sensor: '{sensor.sensor_name}' with id: '{sensor.sensor_id}'", exc_info=e)
                continue

            ## Process the data (or lack thereof) returned from the sensor
            if (data is None):
                self.logger.warning(f"No data read from sensor: '{sensor.sensor_name}' with id: '{sensor.sensor_id}'")
                continue

            if (isinstance(data, list)):
                sensor_data.extend(data)
                self.logger.debug(f"Read from sensor: {sensor.sensor_name} with id: '{sensor.sensor_id}': {[datum.to_dict() for datum in data]}")
            elif (isinstance(data, SensorDatum)):
                sensor_data.append(data)
                self.logger.debug(f"Read from sensor: {sensor.sensor_name} with id: '{sensor.sensor_id}': {data.to_dict()}")

        return sensor_data
