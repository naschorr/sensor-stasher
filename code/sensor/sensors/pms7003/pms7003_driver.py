import asyncio
import logging
from pms7003 import Pms7003Sensor, PmsSensorException
from pathlib import Path
from typing import List

from sensor.sensor_adapter import SensorAdapter
from sensor.models.data.sensor_datum import SensorDatum
from .pms7003_datum import PMS7003Datum
from utilities import load_config, initialize_logging

class PMS7003Driver(SensorAdapter):
    def __init__(self, sensor_id: str):
        config = load_config(Path(__file__).parent)
        self.logger = initialize_logging(logging.getLogger(__name__))

        ## Load config
        self.serial_device_path = config.get('serial_device_path')
        assert (self.serial_device_path is not None)
        self.wakeup_time_seconds: int = config.get('wakeup_time_seconds', 30)

        self._sensor_type = "PMS7003"
        self._sensor_id = sensor_id or self.serial_device_path

        self.sensor = Pms7003Sensor(self.serial_device_path)

        self.logger.debug(f"Initialized {self.sensor_type} sensor. path: '{self.serial_device_path}', id: '{self.sensor_id}', wakeup_time_seconds: '{self.wakeup_time_seconds}'")

    ## Properties

    @property
    def sensor_type(self) -> str:
        return self._sensor_type


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Adapter methods

    async def read(self) -> List[SensorDatum]:
        ## Todo: what if this method is called multiple times within a short interval? This really needs some flavor of lock

        data = {}

        ## Wake the sensor up and spin the fan to get air flowing, and wait for the sensor to move air around
        self.wakeup()
        await asyncio.sleep(self.wakeup_time_seconds)

        ## Read the data from the sensor
        try:
            data = self.sensor.read()
        except PmsSensorException as e:
            self.logger.exception(f"Unable to read sensor with type: '{self.sensor_type}' and id: '{self.sensor_id}'", exc_info=e)
            raise e
        finally:
            ## Put the sensor back to sleep, and shut off the fan
            self.sleep()

        ## Format and return the data
        return [PMS7003Datum(self.sensor_type, self.sensor_id, data)]

    ## Methods

    def wakeup(self):
        with self.sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x01, 0x01, 0x74])
            sensor.write(command)


    def sleep(self):
        with self.sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x00, 0x01, 0x73])
            sensor.write(command)
