import random

from sensor.models.sensor_adapter import SensorAdapter
from sensor.sensors.rng.rng_config import RNGConfig


class RNGDriver(SensorAdapter):
    ## Lifecycle

    def __init__(self, configuration: RNGConfig):
        self._sensor_name = configuration.sensor_name or "RNG"
        self._sensor_id = configuration.sensor_id or self.sensor_name

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
