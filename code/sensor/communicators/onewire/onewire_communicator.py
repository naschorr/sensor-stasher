import contextlib
from pathlib import Path
from abc import ABC

from sensor.models.sensor_type import SensorType
from sensor.models.communicator_adapter import CommunicatorAdapter
from sensor.exceptions.device_in_use_exception import DeviceInUseException


class OneWireCommunicator(CommunicatorAdapter, ABC):
    ## Statics

    ## Keep track of all in use 1-wire device paths to avoid collisions later on
    REGISTERED_ONEWIRE_DEVICES: set[Path] = set()

    ## Properties

    @property
    def sensor_type(self) -> SensorType:
        return SensorType.ONEWIRE

    ## Methods

    @staticmethod
    def register_sensor(serial_device_path: Path):
        if (serial_device_path in OneWireCommunicator.REGISTERED_ONEWIRE_DEVICES):
            raise DeviceInUseException(f"Serial device {serial_device_path} is already in use by another sensor.")

        OneWireCommunicator.REGISTERED_ONEWIRE_DEVICES.add(serial_device_path)


    @staticmethod
    def unregister_sensor(serial_device_path: Path):
        with contextlib.suppress(KeyError):
            OneWireCommunicator.REGISTERED_ONEWIRE_DEVICES.remove(serial_device_path)
