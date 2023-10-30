import asyncio
from pms7003 import Pms7003Sensor, PmsSensorException

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.communicators.serial.raspberrypi.serial_communicator_raspberrypi import SerialCommunicatorRaspberryPi
from sensor.models.data.sensor_measurement import SensorMeasurement
from sensor.platforms.sensors.raspberrypi_sensor import RaspberryPiSensor
from sensor.sensors.pms7003.pms7003_config import PMS7003Config
from sensor.sensors.pms7003.pms7003_measurement import PMS7003Measurement
from sensor.sensors.pms7003.pms7003_driver import PMS7003Driver

class PMS7003DriverRaspberryPi(PMS7003Driver, RaspberryPiSensor, SerialCommunicatorRaspberryPi):
    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, pms7003_configuration: PMS7003Config):
        super(PMS7003Driver).__init__(sensor_stasher_configuration, pms7003_configuration)
        super(SerialCommunicatorRaspberryPi).__init__(self.serial_device_path)

        self._sensor = Pms7003Sensor(self.serial_device_path)

        self.logger.debug(f"Initialized {self.sensor_type} sensor. path: '{self.serial_device_path}', id: '{self.sensor_id}', wakeup_time_seconds: '{self.wakeup_time_seconds}'")

    ## Adapter methods

    async def read(self) -> list[SensorMeasurement]:
        ## Todo: what if this method is called multiple times within a short interval? This really needs some flavor of lock

        data = {}

        ## Wake the sensor up and spin the fan to get air flowing, and wait for the sensor to move air around
        self.wakeup()
        await asyncio.sleep(self.wakeup_time_seconds)

        ## Read the data from the sensor
        try:
            data = self._sensor.read()
        except PmsSensorException as e:
            self.logger.exception(f"Unable to read sensor with type: '{self.sensor_type}' and id: '{self.sensor_id}'", exc_info=e)
            raise e
        finally:
            ## Put the sensor back to sleep, and shut off the fan
            self.sleep()

        ## Format and return the data
        return [PMS7003Measurement(self.sensor_type, self.sensor_id, data)]

    ## Methods

    def wakeup(self):
        with self._sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x01, 0x01, 0x74])
            sensor.write(command)


    def sleep(self):
        with self._sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x00, 0x01, 0x73])
            sensor.write(command)
