from typing import Dict

from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.data.data_type.data_type import DataType


class ExampleSensorDatum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DataType.TEST, sensor_type, sensor_id)

        self.name = measurement.get('name')
        self.example_key = measurement.get('example_key')
