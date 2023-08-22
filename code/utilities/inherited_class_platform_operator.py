from typing import Callable, Optional, Type, TypeVar
import inspect

from sensor.platforms.communicators.platform_communicator import PlatformCommunicator
from sensor.platforms.sensors.platform_sensor import PlatformSensor
from models.platform_type import PlatformType
from sensor.exceptions.sensor_method_finder_platform_exception import SensorMethodFinderPlatformException
from utilities.utilities import get_current_platform

## todo: Is there a better way to organize these one-shot generics?
GenericPlatform = TypeVar('GenericPlatform', bound=PlatformSensor | PlatformCommunicator)


class InheritedClassPlatformOperator:
    ## Methods

    def _find_method_in_object(self, method_to_find: Callable, obj: object) -> Optional[Callable]:
        """
        Find a given method on the provided object. Handy for finding implementations of abstract methods.
        """

        for name, method in inspect.getmembers(obj, predicate=inspect.ismethod):
            if (name == method_to_find.__name__):
                return method


    def _find_platform_implementation_in_object(
                self,
                platform_class: Type[GenericPlatform],
                platform_to_find: PlatformType, obj: object
    ) -> Optional[GenericPlatform]:
        """
        Traverse the inheritance tree (in Module Resolution Order) to find the first platform specific subclass that
        correlates to the provided platform.

        Ex: If some sensor driver inherits from RaspberryPiSensor, and we're looking for a RaspberryPi specific
        PlatformSensor, then this method helps to find specific RaspberryPiSensor without knowing that it's there.

        This also works for other platforms, and other PlatformSensor implementations.
        """

        for cls in obj.__class__.__mro__:
            if (
                    issubclass(cls, platform_class) and
                    cls is not platform_class and
                    cls is not obj.__class__ and
                    platform_to_find.value == cls.get_platform_type().value
            ):
                ## todo: fix return type hinting
                return cls


    def get_sensor_initializer(self, sensor: PlatformSensor) -> Callable:
        """
        Find the sensor initializer method for the current platform on the provided PlatformSensor.
        """

        current_platform = get_current_platform()

        platform_sensor = self._find_platform_implementation_in_object(PlatformSensor, current_platform, sensor)
        if (platform_sensor is None):
            raise SensorMethodFinderPlatformException(f"Unable to find a possible init method for platform: {current_platform} in inherited classes")

        method = self._find_method_in_object(platform_sensor.get_initializer_method(), sensor)
        if (method is not None):
            return method

        raise SensorMethodFinderPlatformException(f"Unable to find a sensor init method for the platform: {current_platform}")


    def get_sensor_reader(self, sensor: PlatformSensor) -> Callable:
        """
        Find the sensor reader method for the current platform on the provided PlatformSensor.
        """

        current_platform = get_current_platform()

        platform_sensor = self._find_platform_implementation_in_object(PlatformSensor, current_platform, sensor)
        if (platform_sensor is None):
            raise SensorMethodFinderPlatformException(f"Unable to find a possible reader method for platform: {current_platform} in inherited classes")

        method = self._find_method_in_object(platform_sensor.get_reader_method(), sensor)
        if (method is not None):
            return method

        raise SensorMethodFinderPlatformException(f"Unable to find a sensor reader method for the platform: {current_platform}")


    def get_communicator_initializer(self, communicator: PlatformCommunicator) -> Callable:
        """
        Find the commumicator initializer method for the current platform on the provided PlatformCommunicator.
        """

        current_platform = get_current_platform()

        platform_communicator = self._find_platform_implementation_in_object(PlatformCommunicator, current_platform, communicator)
        if (platform_communicator is None):
            raise SensorMethodFinderPlatformException(f"Unable to find a possible init method for platform: {current_platform} in inherited classes")

        method = self._find_method_in_object(platform_communicator.get_initializer_method(), communicator)
        if (method is not None):
            return method

        raise SensorMethodFinderPlatformException(f"Unable to find a communicator init method for the platform: {current_platform}")
