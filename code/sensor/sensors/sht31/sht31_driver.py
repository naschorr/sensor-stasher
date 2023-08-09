import logging
import time
from pathlib import Path
from typing import List

from sensor.sensor_types.i2c.i2c_sensor import I2CSensor
from sensor.models.datum.sensor_datum import SensorDatum
from .sht31_datum import SHT31TemperatureDatum, SHT31HumidityDatum
from utilities.utilities import load_config
from utilities.logging.logging import Logging


class SHT31Driver(I2CSensor):
    '''
    Simple interface for the SHT31 temperature and humidity sensor.

    See the datasheet for more information:
    https://sensirion.com/media/documents/213E6A3B/61641DC3/Sensirion_Humidity_Sensors_SHT3x_Datasheet_digital.pdf
    '''

    def __init__(self, sensor_id: str):
        config = load_config(Path(__file__).parent)
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        ## Load config
        self.i2c_bus = int(config.get('i2c_bus', 1))
        assert (self.i2c_bus is not None)
        self.i2c_address = int(config.get('i2c_address', "0x44"), base=16)
        assert (self.i2c_address is not None)
        self.temperature_celcius_offset = config.get('temperature_celcius_offset', 0.0)
        self.humidity_relative_offset = config.get('humidity_relative_offset', 0.0)

        ## Init the i2c sensor
        super().__init__(self.i2c_bus, self.i2c_address)

        self._sensor_type = "SHT31"
        self._sensor_id = sensor_id or f"{self.i2c_bus}-{self.i2c_address}"

        self.logger.debug(f"Initialized {self.sensor_type} sensor. id: {self.sensor_id}, i2c_bus: {self.i2c_bus}, i2c_address: {self.i2c_address}")

    ## Properties

    @property
    def sensor_type(self) -> str:
        return self._sensor_type


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Methods

    def _read_sht3x_data(self) -> List[bytes]:
        '''
        Handles sht3x communications according to the datasheet. Note that this method does one single-shot
        measurement, not a continous series of measurements.
        '''

        ## Initiate single-shot measurement
        self.bus.write_i2c_block_data(self.i2c_address, 0x2C, [0x06])
        ## Give sensor time to process this
        time.sleep(0.5)

        ## Read the raw bytes (6 of them) from the sensor, they are as follows:
        ## [Temperature MSB][Temperature LSB][Temperature CRC][Humidity MSB][Humidity LSB][Humidity CRC]
        return self.bus.read_i2c_block_data(self.i2c_address, 0x00, 6)


    def _extract_temperature_celcius_from_bytes(self, data: List[bytes]) -> float:
        temperature_msb_int = int.from_bytes(data[0], byteorder='big')
        temperature_lsb_int = int.from_bytes(data[1], byteorder='big')

        ## Formula provided by the datasheet
        return -45 + (175 * (temperature_msb_int * 256 + temperature_lsb_int) / 65535.0)


    def _extract_humidity_relative_from_bytes(self, data: List[bytes]) -> float:
        humidity_msb_int = int.from_bytes(data[3], byteorder='big')
        humidity_lsb_int = int.from_bytes(data[4], byteorder='big')

        ## Formula provided by the datasheet
        return 100 * ((humidity_msb_int * 256 + humidity_lsb_int) / 65535.0)

    ## Adapter methods

    async def read(self) -> List[SensorDatum]:
        '''
        Handles the process of initializing the sensor, reading the temperature and humidity data, and formatting it
        into SensorDatum objects, and returning the sensor to an idle state.

        Note that one call to this method returns two datums, one for the temperature, and one for the humidity.
        Separating them helps in later classification, as they can be queried independently from one another.
        '''

        try:
            data = self._read_sht3x_data()
        except Exception as e:
            self.logger.error(f"Failed to interact with {self.sensor_type} - {self.sensor_id} over i2c. {e}")
            return []

        temperature_datum = SHT31TemperatureDatum(self.sensor_type, self.sensor_id, {
            "temperature_celcius": self._extract_temperature_celcius_from_bytes(data) + self.temperature_celcius_offset
        })

        humdity_datum = SHT31HumidityDatum(self.sensor_type, self.sensor_id, {
            "humidity_relative": self._extract_humidity_relative_from_bytes(data) + self.humidity_relative_offset
        })

        return [temperature_datum, humdity_datum]
