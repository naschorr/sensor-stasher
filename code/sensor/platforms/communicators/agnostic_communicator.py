from abc import ABC

from common.models.platform_type import PlatformType
from sensor.platforms.communicators.platform_communicator import PlatformCommunicator


class AgnosticCommunicator(PlatformCommunicator, ABC):

    ## Statics

    @staticmethod
    def get_platform_type() -> PlatformType:
        return PlatformType.AGNOSTIC
