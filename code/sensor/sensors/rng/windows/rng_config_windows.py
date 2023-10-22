from pydantic import Field
from typing import Optional

from sensor.sensors.rng.rng_config import RNGConfig
from sensor.platforms.configurations.windows_config import WindowsConfig


class RNGConfigWindows(RNGConfig, WindowsConfig):
    test: Optional[str] = Field(
        title="Test",
        description="Test",
        default="test"
    )
