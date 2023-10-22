from abc import ABC

from ..platform_base import PlatformBase
from models.platform_type import PlatformType


class RaspberryPiConfig(PlatformBase, ABC):

    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.RASPBERRYPI
