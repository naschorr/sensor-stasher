from pydantic import ConfigDict, Field

from sensor.models.config.sensors.sensor_config import SensorConfig
from sensor.sensor_types.i2c.i2c_sensor_config import I2CSensorConfig
from sensor.models.config.data_type.temperature_sensor_config import TemperatureSensorConfig
from sensor.models.config.data_type.humidity_sensor_config import HumiditySensorConfig


class SHT31Config(SensorConfig, I2CSensorConfig, TemperatureSensorConfig, HumiditySensorConfig):
    model_config = ConfigDict(
        title="SHT31 Configuration"
    )
    wakeup_time_seconds: int = Field(
        default=30,
        description="Time to wait after waking up the sensor before reading data from it."
    )
