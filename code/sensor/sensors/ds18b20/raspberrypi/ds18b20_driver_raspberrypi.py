import os

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.data.sensor_datum import SensorDatum
from sensor.platforms.sensors.raspberrypi_sensor import RaspberryPiSensor
from sensor.sensors.ds18b20.ds18b20_config import DS18B20Config
from sensor.sensors.ds18b20.ds18b20_driver import DS18B20Driver
from sensor.sensors.ds18b20.ds18b20_datum import DS18B20Datum

class DS18B20DriverRaspberryPi(DS18B20Driver, RaspberryPiSensor):
    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, ds18b20_configuration: DS18B20Config):
        super().__init__(sensor_stasher_configuration, ds18b20_configuration)

        ## Load relevant kernel modules for the sensor
        os.system("modprobe w1-gpio")
        os.system("modprobe w1-therm")

        ## Perform initial read to make sure the sensor is ready. Sometimes on startup the sensor will return 85 degrees
        ## celcius, but will fix itself on the next read.
        self.read_one_wire_device_temperature_celcius()

        self.logger.debug(f"Initialized {self.sensor_type} sensor. id: '{self.sensor_id}'")

    ## Adapter methods

    async def read(self) -> list[SensorDatum]:
        temperature_celcius = self.read_one_wire_device_temperature_celcius()

        return [
            DS18B20Datum(self.sensor_type, self.sensor_id, {
                "temperature_celcius": temperature_celcius + self.temperature_celcius_offset
            })
        ]

    ## Methods

    def read_one_wire_device_temperature_celcius(self) -> float:
        with open(self.one_wire_device_path, 'r') as device_file:
            lines = device_file.readlines()
            return float(lines[1].split("=")[1]) / 1000.0
