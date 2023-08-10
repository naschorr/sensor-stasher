from pydantic import BaseModel, Field


class HumiditySensorConfig(BaseModel):
    humidity_relative_offset: float = Field(
        default=0.0,
        description="Offset to apply to the relative humidity reading."
    )
