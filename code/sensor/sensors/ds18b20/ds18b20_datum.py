from typing import Dict

from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.data.data_type.data_type import DataType


class DS18B20Datum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DataType.TEMPERATURE, sensor_type, sensor_id)

        self.temperature_celcius = measurement.get('temperature_celcius')
