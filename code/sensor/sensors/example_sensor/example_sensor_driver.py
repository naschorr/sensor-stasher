from typing import List

from sensor.sensor_adapter import SensorAdapter
from sensor.models.datum.sensor_datum import SensorDatum
from .example_sensor_datum import ExampleSensorDatum


class ExampleSensorDriver(SensorAdapter):
    """
    Simple, system agnostic sensor driver for testing basic functionality without a Raspberry Pi
    """

    def __init__(self, sensor_id: str):
        self._sensor_type = "ExampleSensor"
        self._sensor_id = sensor_id

    ## Properties

    @property
    def sensor_type(self) -> str:
        return self._sensor_type


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Adapter Methods

    async def read(self) -> List[SensorDatum]:
        data = {
            'name': f"{self.sensor_type}-{self.sensor_id}",
            'example_key': 'example_value'
        }

        return ExampleSensorDatum(self.sensor_type, self.sensor_id, data)
