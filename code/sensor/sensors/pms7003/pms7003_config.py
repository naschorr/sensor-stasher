from pydantic import ConfigDict, Field

from sensor.sensor_types.serial.serial_sensor_config import SerialSensorConfig
from sensor.models.data.air_quality_sensor_config import AirQualitySensorConfig


class PMS7003Config(SerialSensorConfig, AirQualitySensorConfig):
    model_config = ConfigDict(
        title="PMS7003 Configuration"
    )
    wakeup_time_seconds: int = Field(
        default=30,
        description="Time to wait after waking up the sensor before reading data from it."
    )
