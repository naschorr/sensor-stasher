from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.data.data_type.data_type import DataType


class SHT31TemperatureDatum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: dict):
        super().__init__(DataType.TEMPERATURE, sensor_type, sensor_id)

        self.temperature_celcius = measurement.get('temperature_celcius')


class SHT31HumidityDatum(SensorDatum):
    def __init__(self, sensor_type: str, sensor_id: str, measurement: dict):
        super().__init__(DataType.HUMIDITY, sensor_type, sensor_id)

        self.humidity_relative = measurement.get('humidity_relative')
