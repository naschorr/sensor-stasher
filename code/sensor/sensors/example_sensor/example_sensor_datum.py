from typing import Dict

from sensor.models.sensor_datum import SensorDatum
from sensor.models.datum_category import DatumCategory


class ExampleSensorDatum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DatumCategory.TEST, sensor_type, sensor_id)

        self.name = measurement.get('name')
        self.example_key = measurement.get('example_key')
