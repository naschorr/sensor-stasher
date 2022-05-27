from typing import Dict

from sensor.sensor_datum import SensorDatum
from sensor.datum_category import DatumCategory


class SHT31TemperatureDatum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DatumCategory.TEMPERATURE, sensor_type, sensor_id)

        self.temperature_celcius = measurement.get('temperature_celcius')


class SHT31HumidityDatum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DatumCategory.HUMIDITY, sensor_type, sensor_id)

        self.humidity_relative = measurement.get('humidity_relative')
