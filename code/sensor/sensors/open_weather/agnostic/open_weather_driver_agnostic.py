import requests

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.communicators.web.web_communicator import WebCommunicator
from sensor.exceptions.sensor_read_exception import SensorReadException
from sensor.models.data.sensor_measurement import SensorMeasurement
from sensor.platforms.sensors.agnostic_sensor import AgnosticSensor
from sensor.sensors.open_weather.open_weather_config import OpenWeatherConfig
from sensor.sensors.open_weather.open_weather_measurement import (
    OpenWeatherVersionMeasurement,
    OpenWeatherLocationMeasurement,
    OpenWeatherTemperatureMeasurement,
    OpenWeatherHumidityMeasurement,
    OpenWeatherAtmosphereMeasurement,
    OpenWeatherPrecipitationMeasurement,
    OpenWeatherPressureMeasurement,
    OpenWeatherWindMeasurement
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

    async def read(self) -> list[SensorMeasurement]:
        ## todo: async
        response = requests.get(self.url, params=self.query_parameters)
        if (response.status_code != 200):
            raise SensorReadException(f"Unable to read {self.sensor_name}, status code: {response.status_code}, response: '{response.text}'")
        data = response.json()

        ## Format and return the data
        return [
            OpenWeatherVersionMeasurement(self.sensor_name, self.sensor_id, OpenWeatherDriver.API_VERSION),
            OpenWeatherLocationMeasurement(self.sensor_name, self.sensor_id, self.latitude, self.longitude),
            OpenWeatherTemperatureMeasurement(self.sensor_name, self.sensor_id, data.get("main")),
            OpenWeatherHumidityMeasurement(self.sensor_name, self.sensor_id, data.get("main").get("humidity")),
            OpenWeatherPressureMeasurement(self.sensor_name, self.sensor_id, data.get("main").get("pressure")),
            OpenWeatherWindMeasurement(self.sensor_name, self.sensor_id, data.get("wind")),
            OpenWeatherAtmosphereMeasurement(self.sensor_name, self.sensor_id, data.get("visibility"), data.get("clouds", {}).get("all")),
            OpenWeatherPrecipitationMeasurement(self.sensor_name, self.sensor_id, data.get("rain", {}), data.get("snow", {}))
        ]
