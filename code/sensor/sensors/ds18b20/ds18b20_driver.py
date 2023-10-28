import os
import logging
from pathlib import Path

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.sensor_adapter import SensorAdapter
from sensor.sensors.ds18b20.ds18b20_config import DS18B20Config
from utilities.logging.logging import Logging

class DS18B20Driver(SensorAdapter):
    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, ds18b20_configuration: DS18B20Config):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        ## Configure
        self.one_wire_device_path = ds18b20_configuration.one_wire_device_path
        self.temperature_celcius_offset = ds18b20_configuration.temperature_celcius_offset or 0.0
        self._sensor_name = ds18b20_configuration.sensor_name or "DS18B20"
        self._sensor_id = ds18b20_configuration.sensor_id or self.one_wire_device_path.parent.name / self.one_wire_device_path.name

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
