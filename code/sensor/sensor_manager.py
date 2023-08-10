import logging
from typing import List, Set

from sensor.sensor_adapter import SensorAdapter
from sensor.models.data.sensor_datum import SensorDatum

from utilities.logging.logging import Logging


class SensorManager:
    def __init__(self):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

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

            ## Process the data (or lack thereof) returned from the sensor
            if (data is None):
                self.logger.warning(f"No data read from sensor type: '{sensor.sensor_type}' with id: '{sensor.sensor_id}'")
                continue

            if (isinstance(data, list)):
                sensor_data.extend(data)
                self.logger.debug(f"Read from {sensor.sensor_type} sensor with id: '{sensor.sensor_id}': {[datum.to_dict() for datum in data]}")
            elif (isinstance(data, SensorDatum)):
                sensor_data.append(data)
                self.logger.debug(f"Read from {sensor.sensor_type} sensor with id: '{sensor.sensor_id}': {data.to_dict()}")

        return sensor_data
