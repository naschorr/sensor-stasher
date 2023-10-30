import pydantic

from common.implementation_instantiator import ImplementationInstantiator
from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.sensor_discoverer import SensorDiscoverer
from sensor.models.sensor_adapter import SensorAdapter
from sensor.models.data.sensor_measurement import SensorMeasurement
from utilities.logging.logging import Logging


class SensorManager:

    ## Lifecycle

    def __init__(
            self,
            logger: Logging,
            configuration: SensorStasherConfig,
            sensors_configuration: pydantic.BaseModel,
            sensor_discoverer: SensorDiscoverer,
            implementation_instantiator: ImplementationInstantiator
    ):
        self.logger = logger
        self.configuration = configuration
        self.sensors_configuration = sensors_configuration
        self.sensor_discoverer = sensor_discoverer
        self.implementation_instantiator = implementation_instantiator

        ## Sensor preparation
        sensor_config_map = self.sensor_discoverer.discover_sensors(self.configuration.sensors_directory_path)
        self._available_sensors: set[SensorAdapter] = set(list(sensor_config_map.keys()))
        self._registered_sensors: set[SensorAdapter] = self.implementation_instantiator.instantiate_classes(
            sensor_config_map,
            self.sensors_configuration
        )

        self.logger.info(f"Initialized {len(self._registered_sensors)} of {len(self._available_sensors)} sensors.")

    ## Properties

    @property
    def available_sensors(self) -> set[SensorAdapter]:
        return self._available_sensors


    @property
    def registered_sensors(self) -> set[SensorAdapter]:
        return self._registered_sensors

    ## Methods

    async def accumulate_all_sensor_data(self) -> list[SensorMeasurement]:
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
                elif (isinstance(data, SensorMeasurement)):
                    sensor_data.append(data)
                    self.logger.debug(f"Read from {sensor.sensor_name} sensor with id: '{sensor.sensor_id}': {data.to_dict()}")
            else:
                self.logger.warning(f"No data read from sensor type: '{sensor.sensor_name}' with id: '{sensor.sensor_id}'")

        return sensor_data
