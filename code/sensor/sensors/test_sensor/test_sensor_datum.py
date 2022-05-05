from typing import Dict

from sensor.sensor_datum import SensorDatum


class TestSensorDatum(SensorDatum):
    def __init__(self, measurement: Dict):
        super().__init__()

        self.key = measurement.get('key')
