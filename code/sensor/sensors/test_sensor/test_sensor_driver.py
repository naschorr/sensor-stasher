from typing import List

from sensor.sensor_adapter import SensorAdapter
from sensor.sensor_datum import SensorDatum
from .test_sensor_datum import TestSensorDatum


class TestSensorDriver(SensorAdapter):
    def __init__(self, sensor_id: str):
        self._sensor_type = "TestSensor"
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
            'test_key': 'test_value'
        }

        return TestSensorDatum(self.sensor_type, self.sensor_id, data)
