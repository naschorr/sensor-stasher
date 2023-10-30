import contextlib
from pathlib import Path
from abc import ABC

from sensor.models.sensor_type import SensorType
from sensor.communicators.models.registerable_communicator_adapter import RegisterableCommunicatorAdapter
from sensor.exceptions.device_in_use_exception import DeviceInUseException


class SerialCommunicator(RegisterableCommunicatorAdapter, ABC):
    ## Statics

    ## Keep track of serial device paths that are in use to avoid collisions later on
    REGISTERED_SERIAL_DEVICES: set[Path] = set()

    ## Properties

    @property
    def sensor_type(self) -> SensorType:
        return SensorType.SERIAL

    ## Methods

    @staticmethod
    def register_sensor(serial_device_path: Path):
        if (serial_device_path in SerialCommunicator.REGISTERED_SERIAL_DEVICES):
            raise DeviceInUseException(f"Serial device {serial_device_path} is already in use by another sensor.")

        SerialCommunicator.REGISTERED_SERIAL_DEVICES.add(serial_device_path)


    @staticmethod
    def unregister_sensor(serial_device_path: Path):
        with contextlib.suppress(KeyError):
            SerialCommunicator.REGISTERED_SERIAL_DEVICES.remove(serial_device_path)
