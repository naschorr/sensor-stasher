import logging
import inspect
import contextlib
import pydantic
from typing import Optional

from sensor.sensor_discoverer import SensorDiscoverer
from models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.sensor_adapter import SensorAdapter
from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.config.sensor_config import SensorConfig
from sensor.exceptions.sensor_init_exception import SensorInitException
from utilities.logging.logging import Logging


class SensorManager:

    ## Lifecycle

    def __init__(
            self,
            logger: Logging,
            configuration: SensorStasherConfig,
            sensors_configuration: pydantic.BaseModel,
            sensor_discoverer: SensorDiscoverer
    ):
        self.logger = logger.initialize_logging(logging.getLogger(__name__))
        self.configuration = configuration
        self.sensors_configuration = sensors_configuration
        self.sensor_discoverer = sensor_discoverer

        ## Sensor preparation
        sensor_config_map = self.sensor_discoverer.discover_sensors(self.configuration.sensors_directory_path)
        self._available_sensors: set[SensorAdapter] = set(list(sensor_config_map.keys()))
        self._registered_sensors: set[SensorAdapter] = self._initialize_sensors(sensor_config_map)

        self.logger.info(f"Initialized {len(self._registered_sensors)} of {len(self._available_sensors)} sensors.")

    ## Properties

    @property
    def available_sensors(self) -> set[SensorAdapter]:
        return self._available_sensors


    @property
    def registered_sensors(self) -> set[SensorAdapter]:
        return self._registered_sensors

    ## Methods

    def _sensor_configuration_retriever(self, sensor_config: SensorConfig) -> Optional[SensorConfig]:
        """
        Attempts to find a configuration property with the same type as the provided sensor configuration class.
        For example: the PMS7003Config sensor config would yield the pms7003 property of the Configuration class.
        """

        for _, cls in inspect.getmembers(self.sensors_configuration):
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


    def _instantiate_sensor_driver(self, driver_class: SensorAdapter, configuration_class: SensorConfig) -> SensorAdapter:
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

        ## Does it have the wrong number of parameters?
        if (len(parameters) != 2):
            raise SensorInitException(f"Invalid number of parameters for sensor: {driver_class.__name__}")

        ## Does it have the expected number of parameters?
        if (len(parameters) == 2):
            ## Make sure we've got a configuration class to work with
            if (configuration is None):
                raise SensorInitException(f"No configuration file provided for sensor: {driver_class.__name__}")

            ## Are the parameters of the expected type? (Don't try and instantiate a sensor that's expecting an int)
            if (
                    parameters[1].annotation is None or
                    (
                        parameters[1].annotation is not None and
                        not issubclass(parameters[1].annotation, SensorConfig)
                    )
            ):
                raise SensorInitException(f"Invalid parameter type for sensor: {driver_class.__name__}, it must inherit from {SensorConfig.__name__} and not {parameters[1].annotation.__name__}")
            
            ## We're all clear to instantiate
            return driver_class(configuration) # type: ignore


    def _initialize_sensors(self, sensor_config_map: dict[SensorAdapter, SensorConfig]) -> set[SensorAdapter]:
        """
        Initialize the available sensors, and inject the relevant configuration property into them (if it exists). Note
        that issues with sensor initialization won't stop the rest from initializing.
        """

        sensors = set()
        for driver_class, configuration_class in sensor_config_map.items():
            try:
                sensor = self._instantiate_sensor_driver(driver_class, configuration_class)
                sensors.add(sensor)
                self.logger.info(f"Successfully initialized sensor: '{sensor.__class__.__name__}' with id: {sensor.sensor_id}")
            except SensorInitException as e:
                ## Couldn't instantiate? No worries, just ignore it and move on
                self.logger.warn(f"Unable to initialize sensor: '{driver_class.__name__}' - {e}")
                continue

        return sensors


    async def accumulate_all_sensor_data(self) -> list[SensorDatum]:
        """
        Look through all registered sensors and read their data. Returns a list of all the sensor data that was read.
        """

        sensor_data = []

        sensor: SensorAdapter
        for sensor in self._registered_sensors:
            data = None
            try:
                data = await sensor.read()
            except Exception as e:
                ## Don't let a single failed sensor read stop the rest
                self.logger.exception(f"Unable to read from sensor type: '{sensor.sensor_name}' with id: '{sensor.sensor_id}'", exc_info=e)
                continue

            if (data is not None):
                if (isinstance(data, list)):
                    sensor_data.extend(data)
                    self.logger.debug(f"Read from {sensor.sensor_name} sensor with id: '{sensor.sensor_id}': {[datum.to_dict() for datum in data]}")
                elif (isinstance(data, SensorDatum)):
                    sensor_data.append(data)
                    self.logger.debug(f"Read from {sensor.sensor_name} sensor with id: '{sensor.sensor_id}': {data.to_dict()}")
            else:
                self.logger.warning(f"No data read from sensor type: '{sensor.sensor_name}' with id: '{sensor.sensor_id}'")

        return sensor_data
