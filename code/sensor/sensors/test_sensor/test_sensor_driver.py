from typing import Dict

from sensor.sensor_adapter import SensorAdapter


class TestSensorDriver(SensorAdapter):
    def __init__(self, config: Dict = None):
        self.name = config.get('name', 'test_sensor')
    

    async def read(self) -> Dict:
        return {
            'name': self.name,
            'test_key': 'test_value'
        }
