import os
import logging
import asyncio
from pathlib import Path

from sensor.models.sensor_adapter import SensorAdapter
from sensor.communicators.onewire.onewire_communicator import OneWireCommunicator
from sensor.platforms.sensors.raspberrypi_sensor import RaspberryPiSensor
from sensor.models.data.sensor_datum import SensorDatum
from sensor.sensors.ds18b20.ds18b20_datum import DS18B20Datum
from sensor.sensors.ds18b20.ds18b20_config import DS18B20Config
from sensor.services.inherited_class_platform_operator import InheritedClassPlatformOperator
from utilities.logging.logging import Logging


class DS18B20Driver(SensorAdapter, OneWireCommunicator, RaspberryPiSensor):
    def __init__(self, configuration: DS18B20Config):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        self.one_wire_device_path = configuration.onewire_device_path
        self.temperature_celcius_offset = configuration.temperature_celcius_offset

        self._sensor_name = "DS18B20"
        self._sensor_id = configuration.sensor_id or self.one_wire_device_path.parent.name or str(self.one_wire_device_path)
        self._initializer = InheritedClassPlatformOperator().get_sensor_initializer(self)
        self._reader = InheritedClassPlatformOperator().get_sensor_reader(self)

        ## Init the 1-wire communicator and the sensor itself for the current platform
        OneWireCommunicator.__init__(self, self.one_wire_device_path)
        task = asyncio.create_task(self._initializer())
        asyncio.get_running_loop().run_until_complete(task)

        self.logger.debug(f"Initialized {self.sensor_type} sensor. id: '{self.sensor_id}'")

    ## Properties

    @property
    def sensor_name(self) -> str:
        return self._sensor_name


    @property
    def sensor_id(self) -> str:
        return self._sensor_id


    @property
    def one_wire_device_path(self) -> Path:
        return self._one_wire_device_path


    @one_wire_device_path.setter
    def one_wire_device_path(self, value):
        if (isinstance(value, Path)):
            self._one_wire_device_path = value
        elif (type(value) is str):
            if (value[0] == "/"):
                try:
                    ## todo: What happens if there are multiple one-wire devices? Is there a smart way to differentiate
                    ## them programatically?
                    self._one_wire_device_path = next(Path("/").glob(value[1:]))
                except StopIteration:
                    raise ValueError(f"Could not find path for '{value}'")
            else:
                ## Can't glob off of a relative path, so just attempt to resolve it normally.
                self._one_wire_device_path = Path(value)
        else:
            raise TypeError(f"one_wire_device_path must be of type Path or str, not {type(value)}")

    ## Methods

    async def read(self) -> list[SensorDatum]:
        return await self._reader()

    ## todo: generalize these for other Linux machines or similar SBCs?

    async def initialize_sensor_raspberrypi(self):
        ## Load the 1-wire temperature sensor kernel module
        os.system("modprobe w1-therm")

        ## Perform initial read to make sure the sensor is ready. Sometimes on startup the sensor will return 85 degrees
        ## celcius, but will fix itself on the next read.
        await self.read_sensor_raspberrypi()


    async def read_sensor_raspberrypi(self) -> list[SensorDatum]:
        temperature_celcius = None
        with open(self.one_wire_device_path, 'r') as device_file:
            lines = device_file.readlines()
            temperature_celcius = float(lines[1].split("=")[1]) / 1000.0

        return [
            DS18B20Datum(self.sensor_type, self.sensor_id, {
                "temperature_celcius": temperature_celcius + self.temperature_celcius_offset
            })
        ]
