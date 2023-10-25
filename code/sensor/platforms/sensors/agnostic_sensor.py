from abc import ABC

from common.models.platform_type import PlatformType
from sensor.platforms.sensors.platform_sensor import PlatformSensor


class AgnosticSensor(PlatformSensor, ABC):
    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.AGNOSTIC
