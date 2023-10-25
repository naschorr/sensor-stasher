import uuid
import platform
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field, DirectoryPath

from utilities.misc import get_root_path
from utilities.logging.log_level import LogLevel


class SensorStasherConfig(BaseModel):
    system_type: Optional[str] = Field(
        default=platform.uname().system.lower(),
        description="The type of system this sensor is running on.",
        examples=["Raspberry Pi Zero 2 W", "Raspberry Pi 4 Model B", "Raspberry Pi 2 Model B"]
    )
    system_id: Optional[str] = Field(
        default=str(uuid.UUID(int=uuid.getnode())),
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
    storage_clients_directory_path: DirectoryPath = Field(
        default=get_root_path() / "code" / "storage" / "clients",
        description="The path to the directory containing storage clients."
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
