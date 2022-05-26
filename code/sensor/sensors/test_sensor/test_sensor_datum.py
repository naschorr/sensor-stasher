from typing import Dict

from sensor.sensor_datum import SensorDatum
from sensor.datum_category import DatumCategory


class TestSensorDatum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DatumCategory.TEST, sensor_type, sensor_id)

        self.test_key = measurement.get('test_key')
