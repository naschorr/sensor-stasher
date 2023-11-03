from typing import Dict

from sensor.models.data.sensor_measurement import SensorMeasurement
from sensor.models.data.data_type.data_type import DataType


class OpenWeatherVersionMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, api_version: str):
        super().__init__(DataType.SCALAR, sensor_name, sensor_id)

        self.api_verion = api_version


class OpenWeatherLocationMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, latitude: float, longitude: float):
        super().__init__(DataType.LOCATION, sensor_name, sensor_id)

        self.latitude = latitude
        self.longitude = longitude


class OpenWeatherTemperatureMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, measurement: Dict):
        super().__init__(DataType.TEMPERATURE, sensor_name, sensor_id)

        self.temperature_c = measurement.get('temp')
        self.temperature_minimum_c = measurement.get('temp_min')
        self.temperature_maximum_c = measurement.get('temp_max')
        self.feels_like_temperature_c = measurement.get('feels_like')


class OpenWeatherHumidityMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, humidity: float):
        super().__init__(DataType.HUMIDITY, sensor_name, sensor_id)

        self.humidity = humidity


class OpenWeatherPressureMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, pressure_sea_level_hpa: float):
        super().__init__(DataType.PRESSURE, sensor_name, sensor_id)

        self.pressure_sea_level_pa = pressure_sea_level_hpa / 100


class OpenWeatherWindMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, measurement: Dict):
        super().__init__(DataType.WIND, sensor_name, sensor_id)

        self.wind_speed_mps = measurement.get('speed')
        self.wind_direction_degrees = measurement.get('deg')
        self.wind_gust_mps = measurement.get('gust')


class OpenWeatherAtmosphereMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, visibility_m: float, cloud_percentage: float):
        super().__init__(DataType.ATMOSPHERE, sensor_name, sensor_id)

        self.visibility_m = visibility_m
        self.cloud_percentage = cloud_percentage


class OpenWeatherPrecipitationMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, rain_measurement: dict, snow_measurement: dict):
        super().__init__(DataType.PRECIPTATION, sensor_name, sensor_id)

        self.rain_1_hour_mm = rain_measurement.get('1h')
        self.rain_3_hour_mm = rain_measurement.get('3h')
        self.snow_1_hour_mm = snow_measurement.get('1h')
        self.snow_3_hour_mm = snow_measurement.get('3h')
