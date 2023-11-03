from abc import ABC

from sensor.models.sensor_type import SensorType
from sensor.communicators.models.communicator_adapter import CommunicatorAdapter


class WebCommunicator(CommunicatorAdapter, ABC):

    ## Properties

    @property
    def sensor_type(self) -> SensorType:
        return SensorType.WEB
