import time

import smbus2    # type: ignore

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.communicators.i2c.raspberrypi.i2c_communicator_raspberrypi import I2CCommunicatorRaspberryPi
from sensor.models.data.sensor_measurement import SensorMeasurement
from sensor.platforms.sensors.raspberrypi_sensor import RaspberryPiSensor
from sensor.sensors.sht31.sht31_measurement import SHT31TemperatureMeasurement, SHT31HumidityMeasurement
from sensor.sensors.sht31.sht31_config import SHT31Config
from sensor.sensors.sht31.sht31_driver import SHT31Driver


class SHT31DriverRaspberryPi(SHT31Driver, RaspberryPiSensor, I2CCommunicatorRaspberryPi):
    '''
    Simple interface for the SHT31 temperature and humidity sensor.

    See the datasheet for more information:
    https://sensirion.com/media/documents/213E6A3B/61641DC3/Sensirion_Humidity_Sensors_SHT3x_Datasheet_digital.pdf
    '''

    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, sht31_configuration: SHT31Config):
        super(SHT31Driver).__init__(sensor_stasher_configuration, sht31_configuration)
        super(I2CCommunicatorRaspberryPi).__init__(self.i2c_bus, self.i2c_address)

        self._bus = smbus2.SMBus(self.i2c_bus)

        self.logger.debug(f"Initialized {self.sensor_type} sensor. id: {self.sensor_id}, i2c_bus: {self.i2c_bus}, i2c_address: {self.i2c_address}")

    ## Methods

    def _read_sht3x_data(self) -> list[bytes]:
        '''
        Handles sht3x communications according to the datasheet. Note that this method does one single-shot
        measurement, not a continous series of measurements.
        '''

        ## Initiate single-shot measurement
        self._bus.write_i2c_block_data(self.i2c_address, 0x2C, [0x06])
        ## Give sensor time to process this
        time.sleep(0.5)

        ## Read the raw bytes (6 of them) from the sensor, they are as follows:
        ## [Temperature MSB][Temperature LSB][Temperature CRC][Humidity MSB][Humidity LSB][Humidity CRC]
        return self._bus.read_i2c_block_data(self.i2c_address, 0x00, 6)

    ## Adapter methods

    async def read(self) -> list[SensorMeasurement]:
        '''
        Handles the process of initializing the sensor, reading the temperature and humidity data, and formatting it
        into SensorMeasurement objects, and returning the sensor to an idle state.

        Note that one call to this method returns two datums, one for the temperature, and one for the humidity.
        Separating them helps in later classification, as they can be queried independently from one another.
        '''

        try:
            data = self._read_sht3x_data()
        except Exception as e:
            self.logger.error(f"Failed to interact with {self.sensor_type} - {self.sensor_id} over i2c. {e}")
            return []

        temperature_measurement = SHT31TemperatureMeasurement(self.sensor_type, self.sensor_id, {
            "temperature_celcius": self._extract_temperature_celcius_from_bytes(data) + self.temperature_celcius_offset
        })

        humdity_measurement = SHT31HumidityMeasurement(self.sensor_type, self.sensor_id, {
            "humidity_relative": self._extract_humidity_relative_from_bytes(data) + self.humidity_relative_offset
        })

        return [temperature_measurement, humdity_measurement]
