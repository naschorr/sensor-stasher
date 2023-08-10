from typing import List

from sensor.sensor_adapter import SensorAdapter
from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.sensor_type import SensorType
from .example_sensor_datum import ExampleSensorDatum


class ExampleSensorDriver(SensorAdapter):
    """
    Simple, system agnostic sensor driver for testing basic functionality without a Raspberry Pi
    """

    def __init__(self, sensor_id: str):
        self._sensor_type = SensorType.HTTP
        self._sensor_name = "Example Sensor"
        self._sensor_id = sensor_id

    ## Properties

    @property
    def sensor_type(self) -> SensorType:
        return self._sensor_type


    @property
    def sensor_name(self) -> str:
        return self._sensor_name


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Adapter Methods

    async def read(self) -> List[SensorDatum]:
        data = {
            'name': f"{self.sensor_type}-{self.sensor_id}",
            'example_key': 'example_value'
        }

        return [ExampleSensorDatum(self.sensor_type, self.sensor_id, data)]
