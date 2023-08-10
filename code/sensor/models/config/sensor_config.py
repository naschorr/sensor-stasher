from typing import Optional
from pydantic import BaseModel, Field


class SensorConfig(BaseModel):
    sensor_id: Optional[str] = Field(
        default=None,
        title="Sensor ID",
        description="A unique identifier for the sensor. If not provided, the sensor will generate it's own unique identifier that may not be static, or easily readable."
    )