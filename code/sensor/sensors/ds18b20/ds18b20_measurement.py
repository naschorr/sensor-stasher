from typing import Dict

from sensor.models.data.sensor_measurement import SensorMeasurement
from sensor.models.data.data_type.data_type import DataType


class DS18B20Measurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, measurement: Dict):
        super().__init__(DataType.TEMPERATURE, sensor_name, sensor_id)

        self.temperature_celcius = measurement.get('temperature_celcius')
