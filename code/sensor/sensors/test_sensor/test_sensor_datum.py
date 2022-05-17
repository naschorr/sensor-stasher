from typing import Dict

from sensor.sensor_datum import SensorDatum
from sensor.sensor_categories import SensorCategories


class TestSensorDatum(SensorDatum):
    def __init__(self, sensor_category: SensorCategories, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(sensor_category, sensor_type, sensor_id)

        self.test_key = measurement.get('test_key')
