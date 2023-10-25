from enum import Enum


class PlatformType(str, Enum):
    AGNOSTIC = "agnostic"
    WINDOWS = "windows"
    WINDOWS_IOT = "windows_iot"
    RASPBERRYPI = "raspberrypi"
    ## Add more as necessary
