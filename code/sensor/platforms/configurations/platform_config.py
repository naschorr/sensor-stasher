from abc import ABC, abstractmethod

from common.models.platform_type import PlatformType
from ..platform_base import PlatformBase


class PlatformConfig(PlatformBase, ABC):

    ## Statics

    @staticmethod
    @abstractmethod
    def get_platform_type() -> PlatformType:
        pass
