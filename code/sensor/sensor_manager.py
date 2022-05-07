from typing import Dict, Set, List

from .sensor_adapter import SensorAdapter
from .sensor_datum import SensorDatum


class SensorManager:
    def __init__(self):
        self.sensors: Set[SensorAdapter] = set()


    def register_sensor(self, sensor: SensorAdapter, sensor_id: str):
        self.sensors.add(sensor(sensor_id))


    async def accumulate_all_sensor_data(self) -> List[SensorDatum]:
        sensor_data = []

        sensor: SensorAdapter
        for sensor in self.sensors:
            data = None
            try:
                data = await sensor.read()
            except Exception as e:
                ## Don't let a single failed sensor read stop the rest
                print(f"Unable to read from sensor '{sensor.sensor_type}-{sensor.sensor_id}': {e}")
                continue

            if (data is not None):
                sensor_data.append(data)

        return sensor_data
