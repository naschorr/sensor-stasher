from enum import Enum


class SensorType(str, Enum):
    I2C = "i2c"
    GPIO = "gpio"
    SPI = "spi"
    ONEWIRE = "1wire"
    SERIAL = "serial"
    USB = "usb"
    WEB = "web"
    MISC = "misc"
