from pydantic import ConfigDict, Field

from sensor.models.config.sensor_config import SensorConfig
from sensor.communicators.serial.serial_sensor_config import SerialSensorConfig
from sensor.models.data.data_type.config.air_quality_sensor_config import AirQualitySensorConfig


class PMS7003Config(SensorConfig, SerialSensorConfig, AirQualitySensorConfig):
    model_config = ConfigDict(
        title="PMS7003 Configuration"
    )
    wakeup_time_seconds: int = Field(
        default=30,
        description="Time to wait after waking up the sensor before reading data from it."
    )
