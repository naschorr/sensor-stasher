from pathlib import Path
from pydantic import BaseModel, Field


class OneWireSensorConfig(BaseModel):
    onewire_device_path: Path = Field(
        title="1-Wire Device Path",
        description="Path to the 1-Wire device."
    )
