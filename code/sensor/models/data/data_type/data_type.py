from enum import Enum


class DataType(str, Enum):
    AIR_QUALITY = "air_quality"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    WIND = "wind"
    PRECIPTATION = "precipitation"
    LIGHT = "light"
    GAS = "gas"
    SOUND = "sound"
    LOCATION = "location"
    TEST = "test"
