from typing import Dict

from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.data.data_type.data_type import DataType

SENSOR_TYPE = "open_weather"


class OpenWeatherVersionDatum(SensorDatum):
    def __init__(self, sensor_id: str, api_version: str):
        super().__init__(DataType.SCALAR, SENSOR_TYPE, sensor_id)

        self.api_verion = api_version


class OpenWeatherLocationDatum(SensorDatum):
    def __init__(self, sensor_id: str, latitude: float, longitude: float):
        super().__init__(DataType.LOCATION, SENSOR_TYPE, sensor_id)

        self.latitude = latitude
        self.longitude = longitude


class OpenWeatherTemperatureDatum(SensorDatum):
    def __init__(self, sensor_id: str, measurement: Dict):
        super().__init__(DataType.TEMPERATURE, SENSOR_TYPE, sensor_id)

        self.temperature_c = measurement.get('temp')
        self.temperature_minimum_c = measurement.get('temp_min')
        self.temperature_maximum_c = measurement.get('temp_max')
        self.feels_like_temperature_c = measurement.get('feels_like')


class OpenWeatherHumidityDatum(SensorDatum):
    def __init__(self, sensor_id: str, humidity: float):
        super().__init__(DataType.HUMIDITY, SENSOR_TYPE, sensor_id)

        self.humidity = humidity


class OpenWeatherPressureDatum(SensorDatum):
    def __init__(self, sensor_id: str, pressure_sea_level_hpa: float):
        super().__init__(DataType.PRESSURE, SENSOR_TYPE, sensor_id)

        self.pressure_sea_level_pa = pressure_sea_level_hpa / 100


class OpenWeatherWindDatum(SensorDatum):
    def __init__(self, sensor_id: str, measurement: Dict):
        super().__init__(DataType.WIND, SENSOR_TYPE, sensor_id)

        self.wind_speed_mps = measurement.get('speed')
        self.wind_direction_degrees = measurement.get('deg')
        self.wind_gust_mps = measurement.get('gust')


class OpenWeatherAtmosphereDatum(SensorDatum):
    def __init__(self, sensor_id: str, visibility_m: float, cloud_percentage: float):
        super().__init__(DataType.ATMOSPHERE, SENSOR_TYPE, sensor_id)

        self.visibility_m = visibility_m
        self.cloud_percentage = cloud_percentage


class OpenWeatherPrecipitationDatum(SensorDatum):
    def __init__(self, sensor_id: str, rain_measurement: dict, snow_measurement: dict):
        super().__init__(DataType.PRECIPTATION, SENSOR_TYPE, sensor_id)

        self.rain_1_hour_mm = rain_measurement.get('1h')
        self.rain_3_hour_mm = rain_measurement.get('3h')
        self.snow_1_hour_mm = snow_measurement.get('1h')
        self.snow_3_hour_mm = snow_measurement.get('3h')
