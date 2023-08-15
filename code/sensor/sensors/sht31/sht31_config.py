from pydantic import ConfigDict, Field

from sensor.models.config.sensor_config import SensorConfig
from sensor.communicators.i2c.i2c_sensor_config import I2CSensorConfig
from sensor.models.data.data_type.config.temperature_sensor_config import TemperatureSensorConfig
from sensor.models.data.data_type.config.humidity_sensor_config import HumiditySensorConfig


class SHT31Config(SensorConfig, I2CSensorConfig, TemperatureSensorConfig, HumiditySensorConfig):
    model_config = ConfigDict(
        title="SHT31 Configuration"
    )
    wakeup_time_seconds: int = Field(
        default=30,
        description="Time to wait after waking up the sensor before reading data from it."
    )
