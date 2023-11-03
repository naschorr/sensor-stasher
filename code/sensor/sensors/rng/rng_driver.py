import random

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.sensor_adapter import SensorAdapter
from sensor.sensors.rng.rng_config import RNGConfig
from utilities.logging.logging import Logging


class RNGDriver(SensorAdapter):
    ## Lifecycle

    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, rng_configuration: RNGConfig):
        self.logger = Logging.LOGGER

        self._sensor_name = rng_configuration.sensor_name or "RNG"
        self._sensor_id = rng_configuration.sensor_id or self.sensor_name

    ## Properties

    @property
    def sensor_name(self) -> str:
        return self._sensor_name


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Methods

    def generate_random_number(self, minimum: float, maximum: float) -> float:
        """
        Generate a random number between the given min and max values.
        """

        return random.random() * (maximum - minimum) + minimum
