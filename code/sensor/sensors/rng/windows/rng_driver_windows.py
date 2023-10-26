import logging

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.sensor_type import SensorType
from sensor.models.data.sensor_datum import SensorDatum
from sensor.sensors.rng.rng_driver import RNGDriver
from sensor.sensors.rng.rng_config import RNGConfig
from sensor.sensors.rng.rng_datum import RNGDatum
from sensor.platforms.sensors.windows_sensor import WindowsSensor
from utilities.logging.logging import Logging


class RNGDriverWindows(RNGDriver, WindowsSensor):
    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, rng_configuration: RNGConfig):
        super().__init__(sensor_stasher_configuration, rng_configuration)

        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        self.max_value = rng_configuration.maximum
        self.min_value = rng_configuration.minimum

        self.logger.debug(f"Initialized sensor: {self.sensor_name} sensor. id: '{self.sensor_id}'")

    ## Methods

    async def read(self) -> list[SensorDatum]:
        return [
            RNGDatum(
                SensorType.MISC,
                self.sensor_id,
                self.generate_random_number(self.min_value, self.max_value)
            )
        ]
