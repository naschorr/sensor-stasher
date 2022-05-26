import logging
import sys
from pathlib import Path
from typing import List

## The recommended Raspberry Pi i2c library doesn't play nice with Windows
## Eventually, with proper orchestration, this check won't be necessary as module will be spun up on demand via
## importlib, and init can be a bit more clever about modules, their capabilities, and their requirements.
if (sys.platform.startswith('linux')):
    import smbus

from sensor.sensor_adapter import SensorAdapter
from sensor.sensor_datum import SensorDatum
from .sht31_datum import SHT31TemperatureDatum, SHT31HumidityDatum
from utilities import load_config, initialize_logging


class SHT31Driver(SensorAdapter):
    def __init__(self, sensor_id: str):
        config = load_config(Path(__file__).parent)
        self.logger = initialize_logging(logging.getLogger(__name__))

        ## Load config
        self.i2c_bus = int(config.get('i2c_bus', 1))
        assert (self.i2c_bus is not None)
        self.i2c_address = hex(config.get('i2c_address', "0x44"))
        assert (self.i2c_address is not None)
        self.temperature_celcius_offset = config.get('temperature_celcius_offset', 0.0)
        self.humidity_relative_offset = config.get('humidity_relative_offset', 0.0)

        self._sensor_type = "SHT31"
        self._sensor_id = sensor_id or f"{self.i2c_bus}-{self.i2c_address}"

        self.bus = smbus.SMBus(self.i2c_bus)
        self.bus.write_i2c_block_data(self.i2c_address, 0x2C, [0x06])

        self.logger.debug(f"Initialized {self.sensor_type} sensor. id: {self.sensor_id}, i2c_bus: {self.i2c_bus}, i2c_address: {self.i2c_address}")

    ## Properties

    @property
    def sensor_type(self) -> str:
        return self._sensor_type


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Adapter methods

    async def read(self) -> List[SensorDatum]:
        try:
            data = self.bus.read_i2c_block_data(self.i2c_address, 0x00, 6)
        except Exception as e:
            self.logger.error(f"Failed to read {self.sensor_type} - {self.sensor_id} over i2c. {e}")
            return None

        temperature_celcius = -45 + (175 * (data[0] * 256 + data[1]) / 65535.0)
        temperature_datum = SHT31TemperatureDatum(self.sensor_type, self.sensor_id, {
            "temperature": temperature_celcius + self.temperature_celcius_offset
        })

        humidity_relative = 100 * (data[3] * 256 + data[4]) / 65535.0
        humdity_datum = SHT31HumidityDatum(self.sensor_type, self.sensor_id, {
            "humidity": humidity_relative + self.humidity_relative_offset
        })

        return [temperature_datum, humdity_datum]
