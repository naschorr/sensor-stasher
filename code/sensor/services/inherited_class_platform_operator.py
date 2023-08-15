from typing import Callable, Optional
import inspect

from sensor.platforms.communicators.platform_communicator import PlatformCommunicator
from sensor.platforms.sensors.platform_sensor import PlatformSensor
from sensor.exceptions.sensor_method_finder_platform_exception import SensorMethodFinderPlatformException
from utilities.utilities import get_current_platform

## todo: simplify this class
class InheritedClassPlatformOperator:
    ## Methods

    def _find_method_in_object(self, method_to_find: Callable, obj: object) -> Optional[Callable]:
        for name, method in inspect.getmembers(obj, predicate=inspect.ismethod):
            if (name == method_to_find.__name__):
                return method


    def get_sensor_initializer(self, sensor: PlatformSensor) -> Callable:
        current_platform = get_current_platform()

        sensor_init_method = None
        for cls in sensor.__class__.__mro__:
            if (
                    issubclass(cls, PlatformSensor) and
                    cls is not PlatformSensor and
                    cls is not sensor.__class__ and
                    current_platform.value == cls.get_platform_type().value
            ):
                sensor_init_method = cls.get_initializer_method()

        if (sensor_init_method is None):
            raise SensorMethodFinderPlatformException(f"Unable to find a possible init method for platform: {current_platform} in inherited classes")

        method = self._find_method_in_object(sensor_init_method, sensor)
        if (method is not None):
            return method

        raise SensorMethodFinderPlatformException(f"Unable to find a sensor init method for the platform: {current_platform}")


    def get_sensor_reader(self, sensor: PlatformSensor) -> Callable:
        current_platform = get_current_platform()

        sensor_reader_method = None
        for cls in sensor.__class__.__mro__:
            if (
                    issubclass(cls, PlatformSensor) and
                    cls is not PlatformSensor and
                    cls is not sensor.__class__ and
                    current_platform.value == cls.get_platform_type().value
            ):
                sensor_reader_method = cls.get_reader_method()

        if (sensor_reader_method is None):
            raise SensorMethodFinderPlatformException(f"Unable to find a possible reader method for platform: {current_platform} in inherited classes")

        method = self._find_method_in_object(sensor_reader_method, sensor)
        if (method is not None):
            return method

        raise SensorMethodFinderPlatformException(f"Unable to find a sensor reader method for the platform: {current_platform}")


    def get_communicator_initializer(self, communicator: PlatformCommunicator) -> Callable:
        current_platform = get_current_platform()

        communicator_init_method = None
        for cls in communicator.__class__.__mro__:
            if (
                    issubclass(cls, PlatformSensor) and
                    cls is not PlatformSensor and
                    cls is not communicator.__class__ and
                    current_platform.value == cls.get_platform_type().value
            ):
                communicator_init_method = cls.get_reader_method()

        if (communicator_init_method is None):
            raise SensorMethodFinderPlatformException(f"Unable to find a possible init method for platform: {current_platform} in inherited classes")

        method = self._find_method_in_object(communicator_init_method, communicator)
        if (method is not None):
            return method

        raise SensorMethodFinderPlatformException(f"Unable to find a communicator init method for the platform: {current_platform}")
