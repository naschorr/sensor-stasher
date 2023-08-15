from pydantic import ConfigDict

from sensor.models.config.sensor_config import SensorConfig
from sensor.models.data.data_type.config.temperature_sensor_config import TemperatureSensorConfig
from sensor.communicators.onewire.onewire_sensor_config import OneWireSensorConfig


class DS18B20Config(SensorConfig, OneWireSensorConfig, TemperatureSensorConfig):
    model_config = ConfigDict(
        title="DS18B20 Configuration"
    )
