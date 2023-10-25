from pydantic import Field
from typing import Optional

from sensor.sensors.rng.rng_config import RNGConfig
from sensor.platforms.configurations.windows_config import WindowsConfig


class RNGConfigWindows(RNGConfig, WindowsConfig):
    sensor_id_affix: Optional[str] = Field(
        title="Sensor ID Affix",
        description="String to affix to the sensor's ID",
        default=None
    )
