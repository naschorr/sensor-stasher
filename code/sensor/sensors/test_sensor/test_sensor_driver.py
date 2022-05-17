from typing import Dict

from sensor.sensor_adapter import SensorAdapter
from sensor.sensor_datum import SensorDatum
from sensor.sensor_categories import SensorCategories
from .test_sensor_datum import TestSensorDatum


class TestSensorDriver(SensorAdapter):
    def __init__(self, sensor_id: str):
        self._sensor_category = SensorCategories.TEST
        self._sensor_type = "TestSensor"
        self._sensor_id = sensor_id
    
    ## Properties

    @property
    def sensor_category(self) -> SensorCategories:
        return self._sensor_category


    @property
    def sensor_type(self):
        return self._sensor_type


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Adapter Methods

    async def read(self) -> SensorDatum:
        data = {
            'name': f"{self.sensor_type}-{self.sensor_id}",
            'test_key': 'test_value'
        }

        return TestSensorDatum(self.sensor_category, self.sensor_type, self.sensor_id, data)
