from typing import Optional
from pydantic import ConfigDict, Field

from sensor.models.config.sensor_config import SensorConfig


class OpenWeatherConfig(SensorConfig):  ## todo: weather data base configs
    model_config = ConfigDict(
        title="OpenWeather Configuration"
    )
    latitude: float = Field(
        title="Latitude",
        description="Latitude of the location to get weather data for.",
        example=47.578407901391955,
        ge=-90,
        le=90
    )
    longitude: float = Field(
        title="Longitude",
        description="Longitude of the location to get weather data for.",
        example=-121.97813275174478,
        ge=-180,
        le=180
    )
    app_id: str = Field(
        title="App ID",
        description="The app ID to use to access the OpenWeather API."
    )
    exclude: Optional[list[str]] = Field(
        default=[],
        title="Exclude",
        description="The data types to exclude from the OpenWeather API response.",
        example=["minutely", "hourly", "daily", "alerts"]
    )
