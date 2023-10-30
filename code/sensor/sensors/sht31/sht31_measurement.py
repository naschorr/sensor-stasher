from typing import Dict

from sensor.models.data.sensor_measurement import SensorMeasurement
from sensor.models.data.data_type.data_type import DataType


class SHT31TemperatureMeasurement(SensorMeasurement):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DataType.TEMPERATURE, sensor_type, sensor_id)

        self.temperature_celcius = measurement.get('temperature_celcius')


class SHT31HumidityMeasurement(SensorMeasurement):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DataType.HUMIDITY, sensor_type, sensor_id)

        self.humidity_relative = measurement.get('humidity_relative')
