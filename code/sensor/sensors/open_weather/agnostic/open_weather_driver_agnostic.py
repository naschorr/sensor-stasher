import requests

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.communicators.web.web_communicator import WebCommunicator
from sensor.exceptions.sensor_read_exception import SensorReadException
from sensor.models.data.sensor_datum import SensorDatum
from sensor.platforms.sensors.agnostic_sensor import AgnosticSensor
from sensor.sensors.open_weather.open_weather_config import OpenWeatherConfig
from sensor.sensors.open_weather.open_weather_datum import (
    OpenWeatherVersionDatum,
    OpenWeatherLocationDatum,
    OpenWeatherTemperatureDatum,
    OpenWeatherHumidityDatum,
    OpenWeatherAtmosphereDatum,
    OpenWeatherPrecipitationDatum,
    OpenWeatherPressureDatum,
    OpenWeatherWindDatum
)
from sensor.sensors.open_weather.open_weather_driver import OpenWeatherDriver

class OpenWeatherDriverAgnostic(OpenWeatherDriver, AgnosticSensor, WebCommunicator):

    ## Lifecycle

    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, open_weather_configuration: OpenWeatherConfig):
        super().__init__(sensor_stasher_configuration, open_weather_configuration)

        self.url = OpenWeatherDriver.BASE_URL
        self.query_parameters = self._build_query_parameters()

        self.logger.debug(f"Initialized {self.sensor_name} sensor. Latitude: '{self.latitude}', longitude: '{self.longitude}'")

    ## Methods

    def _build_query_parameters(self) -> dict:
        ## Build the query params
        query_params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "appid": self.app_id,
            "units": "metric"
        }
        if (self.exclude):
            query_params["exclude"] = self.exclude

        return query_params

    ## Adapter methods

    async def read(self) -> list[SensorDatum]:
        ## todo: async
        response = requests.get(self.url, params=self.query_parameters)
        if (response.status_code != 200):
            raise SensorReadException(f"Unable to read {self.sensor_name}, status code: {response.status_code}, response: '{response.text}'")
        data = response.json()

        ## Format and return the data
        return [
            OpenWeatherVersionDatum(self.sensor_id, OpenWeatherDriver.API_VERSION),
            OpenWeatherLocationDatum(self.sensor_id, self.latitude, self.longitude),
            OpenWeatherTemperatureDatum(self.sensor_id, data.get("main")),
            OpenWeatherHumidityDatum(self.sensor_id, data.get("main").get("humidity")),
            OpenWeatherPressureDatum(self.sensor_id, data.get("main").get("pressure")),
            OpenWeatherWindDatum(self.sensor_id, data.get("wind")),
            OpenWeatherAtmosphereDatum(self.sensor_id, data.get("visibility"), data.get("clouds", {}).get("all")),
            OpenWeatherPrecipitationDatum(self.sensor_id, data.get("rain", {}), data.get("snow", {}))
        ]
