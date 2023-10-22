from abc import ABC

from .platform_config import PlatformConfig
from models.platform_type import PlatformType


class WindowsConfig(PlatformConfig, ABC):

    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.WINDOWS
