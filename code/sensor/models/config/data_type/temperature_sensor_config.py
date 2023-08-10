from pydantic import BaseModel, Field


class TemperatureSensorConfig(BaseModel):
    temperature_celcius_offset: float = Field(
        default=0.0,
        description="Offset to apply to the temperature reading in degrees celcius."
    )
