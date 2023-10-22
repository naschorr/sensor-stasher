from abc import ABC, abstractmethod

from ..platform_base import PlatformBase
from models.platform_type import PlatformType


class PlatformConfig(PlatformBase, ABC):

    ## Statics

    @staticmethod
    @abstractmethod
    def get_platform_type() -> PlatformType:
        pass
