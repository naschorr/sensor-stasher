from typing import Dict

from sensor.models.datum.sensor_datum import SensorDatum
from sensor.models.datum.datum_category import DatumCategory


class DS18B20Datum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: Dict):
        super().__init__(DatumCategory.TEMPERATURE, sensor_type, sensor_id)

        self.temperature_celcius = measurement.get('temperature_celcius')
