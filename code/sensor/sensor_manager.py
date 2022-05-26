import logging
from typing import Set, List

from .sensor_adapter import SensorAdapter
from .sensor_datum import SensorDatum

from utilities import initialize_logging


class SensorManager:
    def __init__(self):
        self.logger = initialize_logging(logging.getLogger(__name__))

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
                self.logger.exception(f"Unable to read from sensor type: '{sensor.sensor_type}' with id: '{sensor.sensor_id}'", exc_info=e)
                continue

            if (data is not None):
                if (isinstance(data, list)):
                    sensor_data.extend(data)
                elif (isinstance(data, SensorDatum)):
                    sensor_data.append(data)

        return sensor_data
