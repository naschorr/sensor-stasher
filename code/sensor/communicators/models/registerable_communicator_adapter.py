from abc import ABC, abstractmethod

from sensor.communicators.models.communicator_adapter import CommunicatorAdapter


class RegisterableCommunicatorAdapter(CommunicatorAdapter, ABC):
    
    ## Statics

    @staticmethod
    @abstractmethod
    def register_sensor(*args):
        pass


    @staticmethod
    @abstractmethod
    def unregister_sensor(*args):
        pass
