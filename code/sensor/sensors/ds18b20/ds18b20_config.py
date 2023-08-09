from pydantic import ConfigDict

from sensor.models.data.temperature_sensor_config import TemperatureSensorConfig
from sensor.sensor_types.onewire.onewire_sensor_config import OneWireSensorConfig


class DS18B20Config(OneWireSensorConfig, TemperatureSensorConfig):
    model_config = ConfigDict(
        title="DS18B20 Configuration"
    )
