from pathlib import Path
from pydantic import BaseModel, Field


class SerialSensorConfig(BaseModel):
    serial_device_path: Path = Field(
        title="Serial Device Path",
        description="Path to the Serial device."
    )
