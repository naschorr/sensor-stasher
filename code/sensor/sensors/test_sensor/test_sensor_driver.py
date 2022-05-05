from typing import Dict

from sensor.sensor_adapter import SensorAdapter


class TestSensorDriver(SensorAdapter):
    def __init__(self, config: Dict = None):
        self.config = config
    

    async def read(self) -> Dict:
        return {'test_key': 'test_value'}
