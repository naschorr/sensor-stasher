from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field

from utilities.logging.log_level import LogLevel
from utilities.misc import get_root_path


class LoggingConfig(BaseModel):
    log_level: LogLevel = Field(
        default=LogLevel.INFO,
        title="Log Level",
        description="The log level to use for the application."
    )
    log_path: Optional[Path] = Field(
        default=get_root_path() / 'logs',
        title="Log Path",
        description="The path to the logging directory for the application."
    )
    log_backup_count: int = Field(
        default=7,
        title="Log Backup Count",
        description="The number of log files to keep."
    )
    log_name: str = Field(
        default="sensor_stasher",
        title="Log File Name",
        description="The name of the log file."
    )
