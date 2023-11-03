from abc import ABC

from common.models.platform_type import PlatformType
from .platform_config import PlatformConfig


class RaspberryPiConfig(PlatformConfig, ABC):

    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.RASPBERRYPI
