import time
from pms7003 import Pms7003Sensor, PmsSensorException
from typing import Dict

from code.sensor.sensor_adapter import SensorAdapter
from .pms7003_datum import PMS7003_Datum


class PMS7003_Driver(SensorAdapter):
    def __init__(self, path=None):
        if(path is None):
            ## Assuming we're on a Raspberry Pi, this is the default path to the serial device
            path = '/dev/serial0'

        self.sensor = Pms7003Sensor(path)
    
    ## Adapter methods

    async def read(self) -> Dict:
        data = {}

        ## Wake the sensor up and spin the fan to get air flowing, and wait for the sensor to move air around
        self.wakeup()
        time.sleep(30)

        ## Read the data from the sensor
        try:
            data = self.sensor.read()
        except PmsSensorException as e:
            print(f'Unable to read PMS7003 sensor data: {e}')
            raise e
        finally:
            ## Put the sensor back to sleep, and shut off the fan
            self.sleep()
        
        ## Format and return the data
        return PMS7003_Datum(data).to_dict()

    ## Methods

    def wakeup(self):
        with self.sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x01, 0x01, 0x74])
            sensor.write(command)


    def sleep(self):
        with self.sensor._serial as sensor:
            command = bytearray([0x42, 0x4D, 0xE4, 0x00, 0x00, 0x01, 0x73])
            sensor.write(command)
