from pydantic import BaseModel, Field


class AirQualitySensorConfig(BaseModel):
    pm1_0cf1_offset: int = Field(
        default=0,
        title="PM1.0 CF=1 Offset",
        description="Offset to apply to PM1.0 CF=1 measurements."
    )
    pm2_5cf1_offset: int = Field(
        default=0,
        title="PM2.5 CF=1 Offset",
        description="Offset to apply to PM2.5 CF=1 measurements."
    )
    pm10cf1_offset: int = Field(
        default=0,
        title="PM10 CF=1 Offset",
        description="Offset to apply to PM10 CF=1 measurements."
    )

    pm1_0sat_offset: int = Field(
        default=0,
        title="PM1.0 Standard Atmosphere Offset",
        description="Offset to apply to PM1.0 Standard Atmosphere measurements."
    )
    pm2_5sat_offset: int = Field(
        default=0,
        title="PM2.5 Standard Atmosphere Offset",
        description="Offset to apply to PM2.5 Standard Atmosphere measurements."
    )
    pm10sat_offset: int = Field(
        default=0,
        title="PM10 Standard Atmosphere Offset",
        description="Offset to apply to PM10 Standard Atmosphere measurements."
    )

    n0_3_offset: int = Field(
        default=0,
        title="N0.3 Offset",
        description="Offset to apply to Number of Particles > 0.3 µm measurements."
    )
    n0_5_offset: int = Field(
        default=0,
        title="N0.5 Offset",
        description="Offset to apply to Number of Particles > 0.5 µm measurements."
    )
    n1_0_offset: int = Field(
        default=0,
        title="N1.0 Offset",
        description="Offset to apply to Number of Particles > 1.0 µm measurements."
    )
    n2_5_offset: int = Field(
        default=0,
        title="N2.5 Offset",
        description="Offset to apply to Number of Particles > 2.5 µm measurements."
    )
    n5_0_offset: int = Field(
        default=0,
        title="N5.0 Offset",
        description="Offset to apply to Number of Particles > 5.0 µm measurements."
    )
    n10_offset: int = Field(
        default=0,
        title="N10 Offset",
        description="Offset to apply to Number of Particles > 10 µm measurements."
    )
