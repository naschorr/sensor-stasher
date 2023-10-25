from abc import ABC

from sensor.platforms.sensors.platform_sensor import PlatformSensor
from models.platform_type import PlatformType


class WindowsSensor(PlatformSensor, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.WINDOWS
