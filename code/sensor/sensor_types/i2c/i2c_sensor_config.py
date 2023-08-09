from pydantic import BaseModel, Field


class I2CSensorConfig(BaseModel):
    i2c_bus: int = Field(
        title="I2C Bus",
        description="The I2C bus to use.",
    )
    i2c_address: int = Field(
        title="I2C Address",
        description="The I2C address to use."
    )
