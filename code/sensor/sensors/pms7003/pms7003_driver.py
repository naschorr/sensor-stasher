import asyncio
import logging
from pms7003 import Pms7003Sensor, PmsSensorException
from typing import List

from sensor.models.sensor_adapter import SensorAdapter
from sensor.communicators.serial.serial_communicator import SerialCommunicator
from sensor.platforms.sensors.raspberrypi_sensor import RaspberryPiSensor
from sensor.models.data.sensor_datum import SensorDatum
from sensor.sensors.pms7003.pms7003_datum import PMS7003Datum
from sensor.sensors.pms7003.pms7003_config import PMS7003Config
from utilities.inherited_class_platform_operator import InheritedClassPlatformOperator
from utilities.logging.logging import Logging


class PMS7003Driver(SensorAdapter, SerialCommunicator, RaspberryPiSensor):
    def __init__(self, configuration: PMS7003Config):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        self.serial_device_path = configuration.serial_device_path
        self.wakeup_time_seconds = configuration.wakeup_time_seconds

        self._sensor_name = "PMS7003"
        self._sensor_id = configuration.sensor_id or str(self.serial_device_path)
        self._reader = InheritedClassPlatformOperator().get_sensor_reader(self)

        ## Init the serial communicator and the sensor itself
        SerialCommunicator.__init__(self, self.serial_device_path)
        self.sensor = Pms7003Sensor(self.serial_device_path)

        self.logger.debug(f"Initialized {self.sensor_type} sensor. path: '{self.serial_device_path}', id: '{self.sensor_id}', wakeup_time_seconds: '{self.wakeup_time_seconds}'")

    ## Properties

    @property
    def sensor_name(self) -> str:
        return self._sensor_name


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Methods

    async def read(self) -> List[SensorDatum]:
        return await self._reader()


    async def read_sensor_raspberrypi(self) -> List[SensorDatum]:
        ## Lock to prevent multiple wakeup -> read -> sleep cycles from happening at the same time
        lock = asyncio.Lock()

        async with lock:
            ## Wake the sensor up and spin the fan to get air flowing, and wait for the sensor to move air around
            self.wakeup()
            await asyncio.sleep(self.wakeup_time_seconds)

            ## Read the data from the sensor
            data = {}
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


    def wakeup(self):
        with self.sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x01, 0x01, 0x74])
            sensor.write(command)


    def sleep(self):
        with self.sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x00, 0x01, 0x73])
            sensor.write(command)
