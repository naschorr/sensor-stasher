from abc import ABC, abstractmethod

from models.platform_type import PlatformType


class PlatformBase(ABC):
    ## Statics

    @staticmethod
    @abstractmethod
    def get_platform_type() -> PlatformType:
        pass
