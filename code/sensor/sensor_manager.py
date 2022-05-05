from typing import Dict, Set

from .sensor_adapter import SensorAdapter


class SensorManager:
    def __init__(self):
        self.sensors: Set[SensorAdapter] = set()


    def register_sensor(self, sensor: SensorAdapter, config: Dict = None):
        if config is None:
            config = {}

        self.sensors.add(sensor(config))


    async def _accumulate_all_sensor_data(self):
        sensor_data = []

        sensor: SensorAdapter
        for sensor in self.sensors:
            sensor_data.append(await sensor.read())

        return sensor_data
