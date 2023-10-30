from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.models.sensor_adapter import SensorAdapter
from sensor.sensors.open_weather.open_weather_config import OpenWeatherConfig
from utilities.logging.logging import Logging

class OpenWeatherDriver(SensorAdapter):
    
    ## Statics

    API_VERSION = "2.5"
    BASE_URL = f"https://api.openweathermap.org/data/{API_VERSION}/weather"

    ## Lifecycle

    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, open_weather_configuration: OpenWeatherConfig):
        self.logger = Logging.LOGGER

        ## Configure
        self.latitude = open_weather_configuration.latitude
        self.longitude = open_weather_configuration.longitude
        self.app_id = open_weather_configuration.app_id
        self.exclude = open_weather_configuration.exclude or []
        self._sensor_name = open_weather_configuration.sensor_name or "open_weather"
        self._sensor_id = open_weather_configuration.sensor_id or f"{self.sensor_name}/{self.latitude}/{self.longitude}"

    ## Properties

    @property
    def sensor_name(self) -> str:
        return self._sensor_name


    @property
    def sensor_id(self) -> str:
        return self._sensor_id
