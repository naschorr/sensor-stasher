from pydantic import ConfigDict

from sensor.models.config.sensors.sensor_config import SensorConfig
from sensor.models.config.data_type.temperature_sensor_config import TemperatureSensorConfig
from sensor.sensor_types.onewire.onewire_sensor_config import OneWireSensorConfig


class DS18B20Config(SensorConfig, OneWireSensorConfig, TemperatureSensorConfig):
    model_config = ConfigDict(
        title="DS18B20 Configuration"
    )
