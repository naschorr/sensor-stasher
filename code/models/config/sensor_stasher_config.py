from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field, DirectoryPath

from sensor.sensors.ds18b20.ds18b20_config import DS18B20Config
from sensor.sensors.pms7003.pms7003_config import PMS7003Config
from sensor.sensors.sht31.sht31_config import SHT31Config
from sensor.sensors.rng.rng_config import RNGConfig
from storage.clients.influx.influxdb_config import InfluxDBConfig
from utilities.misc import get_root_path
from utilities.logging.log_level import LogLevel


class SensorStasherConfig(BaseModel):
    ## SensorStasher Configuration
    system_type: Optional[str] = Field(
        default=None,
        description="The type of system this sensor is running on.",
        examples=["Raspberry Pi Zero 2 W", "Raspberry Pi 4 Model B", "Raspberry Pi 2 Model B"]
    )
    system_id: Optional[str] = Field(
        default=None,
        description="The unique ID of the system this sensor is running on.",
        examples=["Living Room", "Bedroom", "Office 0", "Office 1"]
    )
    sensor_poll_interval_seconds: int = Field(
        default=300,
        description="The number of seconds to wait between polling sensors."
    )
    sensors_directory_path: DirectoryPath = Field(
        default=get_root_path() / "code" / "sensor" / "sensors",
        description="The path to the directory containing sensor implementations."
    )
    log_level: LogLevel = Field(
        default=LogLevel.ERROR,
        title="Log Level",
        description="The log level to use for the application."
    )
    log_path: Optional[Path] = Field(
        default=None,
        title="Log Path",
        description="The path to the logging directory for the application."
    )
    log_backup_count: int = Field(
        default=7,
        description="The number of log files to keep."
    )

    # ## Sensor Configuration
    # ds18b20: Optional[DS18B20Config] = Field(
    #     default=None,
    #     title="DS18B20 Sensor",
    #     description="Configuration for the DS18B20 temperature sensor."
    # )
    # pms7003: Optional[PMS7003Config] = Field(
    #     default=None,
    #     title="PMS7003 Sensor",
    #     description="Configuration for the PMS7003 air quality sensor."
    # )
    # sht31: Optional[SHT31Config] = Field(
    #     default=None,
    #     title="SHT31 Sensor",
    #     description="Configuration for the SHT31 temperature and humidity sensor."
    # )
    # rng: Optional[RNGConfig] = Field(
    #     default=None,
    #     title="RNG Sensor",
    #     description="Configuration for the RNG sensor."
    # )

    ## Storage Configuration
    influxdb: Optional[InfluxDBConfig] = Field(
        default=None,
        title="InfluxDB",
        description="Configuration for the InfluxDB storage client."
    )