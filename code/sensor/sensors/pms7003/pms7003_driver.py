import asyncio
from pms7003 import Pms7003Sensor, PmsSensorException
from pathlib import Path

from sensor.sensor_adapter import SensorAdapter
from sensor.sensor_datum import SensorDatum
from sensor.sensor_categories import SensorCategories
from .pms7003_datum import PMS7003Datum
from config import load_config

class PMS7003Driver(SensorAdapter):
    def __init__(self, sensor_id: str):
        config = load_config(Path(__file__).parent)

        self.serial_device_path = config.get('serial_device_path')
        self.wakeup_time_seconds: int = config.get('wakeup_time_seconds', 30)
        self._sensor_category = SensorCategories.AIR_QUALITY
        self._sensor_type = "PMS7003"
        self._sensor_id = sensor_id if sensor_id is not None else self.serial_device_path

        self.sensor = Pms7003Sensor(self.serial_device_path)
    
    ## Properties

    @property
    def sensor_category(self) -> SensorCategories:
        return self._sensor_category


    @property
    def sensor_type(self):
        return self._sensor_type


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Adapter methods

    async def read(self) -> SensorDatum:
        ## Todo: what if this method is called multiple times within a short interval? This really needs some flavor of lock

        data = {}

        ## Wake the sensor up and spin the fan to get air flowing, and wait for the sensor to move air around
        self.wakeup()
        await asyncio.sleep(self.wakeup_time_seconds)

        ## Read the data from the sensor
        try:
            data = self.sensor.read()
        except PmsSensorException as e:
            print(f'Unable to read {self.sensor_type} sensor data: {e}')
            raise e
        finally:
            ## Put the sensor back to sleep, and shut off the fan
            self.sleep()
        
        ## Format and return the data
        return PMS7003Datum(self.sensor_category, self.sensor_type, self.sensor_id, data)

    ## Methods

    def wakeup(self):
        with self.sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x01, 0x01, 0x74])
            sensor.write(command)


    def sleep(self):
        with self.sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x00, 0x01, 0x73])
            sensor.write(command)
