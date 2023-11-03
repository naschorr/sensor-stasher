from pydantic import BaseModel, Field


class I2CSensorConfig(BaseModel):
    i2c_bus: int = Field(
        title="I2C Bus",
        description="The I2C bus to use.",
    )
    i2c_address: str = Field(
        title="I2C Address",
        description="The hexadecimal I2C address to use.",
        examples=["0x44", "0x69", "0x1f"]
    )
