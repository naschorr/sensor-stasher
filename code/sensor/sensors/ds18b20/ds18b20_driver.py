import os
import logging
from pathlib import Path
from typing import List

from sensor.sensor_types.onewire.onewire_sensor import OneWireSensor
from sensor.models.datum.sensor_datum import SensorDatum
from .ds18b20_datum import DS18B20Datum
from utilities.utilities import load_config
from utilities.logging.logging import Logging


class DS18B20Driver(OneWireSensor):
    def __init__(self, sensor_id: str):
        config = load_config(Path(__file__).parent)
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        ## Load config
        self.one_wire_device_path = config.get('one_wire_device_path')
        assert (self.one_wire_device_path is not None)
        self.temperature_celcius_offset = config.get('temperature_celcius_offset', 0.0)

        self._sensor_name = "DS18B20"
        self._sensor_id = sensor_id or self.one_wire_device_path.parent.name or self.one_wire_device_path

        ## Load the 1-wire temperature sensor kernel module
        os.system("modprobe w1-therm")

        ## Perform initial read to make sure the sensor is ready. Sometimes on startup the sensor will return 85 degrees
        ## celcius, but will fix itself on the next read.
        self.read_one_wire_device_temperature_celcius()

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
        if (type(value) is Path):
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

    ## Adapter methods

    async def read(self) -> List[SensorDatum]:
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
