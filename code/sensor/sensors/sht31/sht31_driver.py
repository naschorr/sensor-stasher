from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.sensor_adapter import SensorAdapter
from sensor.sensors.sht31.sht31_config import SHT31Config
from utilities.logging.logging import Logging


class SHT31Driver(SensorAdapter):
    '''
    Simple interface for the SHT31 temperature and humidity sensor.

    See the datasheet for more information:
    https://sensirion.com/media/documents/213E6A3B/61641DC3/Sensirion_Humidity_Sensors_SHT3x_Datasheet_digital.pdf
    '''

    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, sht31_configuration: SHT31Config):
        self.logger = Logging.LOGGER

        ## Configure
        self.i2c_bus = sht31_configuration.i2c_bus
        self.i2c_address = sht31_configuration.i2c_address
        self.temperature_celcius_offset = sht31_configuration.temperature_celcius_offset or 0.0
        self.humidity_relative_offset = sht31_configuration.humidity_relative_offset or 0.0
        self._sensor_name = sht31_configuration.sensor_name or "SHT31"
        self._sensor_id = sht31_configuration.sensor_id or f"{self.i2c_bus}-{self.i2c_address}"

        self.logger.debug(f"Initialized {self.sensor_type} sensor. id: {self.sensor_id}, i2c_bus: {self.i2c_bus}, i2c_address: {self.i2c_address}")

    ## Properties

    @property
    def sensor_name(self) -> str:
        return self._sensor_name


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

    ## Methods

    def _extract_temperature_celcius_from_bytes(self, data: list[bytes]) -> float:
        temperature_msb = data[0]
        temperature_lsb = data[1]

        ## Formula provided by the datasheet
        return -45 + (175 * (temperature_msb * 256 + temperature_lsb) / 65535.0)


    def _extract_humidity_relative_from_bytes(self, data: list[bytes]) -> float:
        humidity_msb = data[3]
        humidity_lsb = data[4]

        ## Formula provided by the datasheet
        return 100 * ((humidity_msb * 256 + humidity_lsb) / 65535.0)
