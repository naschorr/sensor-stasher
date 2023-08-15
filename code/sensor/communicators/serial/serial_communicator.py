import logging
import os
from pathlib import Path
import contextlib

from sensor.models.sensor_type import SensorType
from sensor.models.communicator_adapter import CommunicatorAdapter
from sensor.platforms.communicators.raspberrypi_communicator import RaspberryPiCommunicator
from sensor.services.inherited_class_platform_operator import InheritedClassPlatformOperator
from sensor.exceptions.device_in_use_exception import DeviceInUseException
from utilities.logging.logging import Logging


class SerialCommunicator(CommunicatorAdapter, RaspberryPiCommunicator):
    ## Statics

    ## Keep track of serial device paths that are in use to avoid collisions later on
    REGISTERED_SERIAL_DEVICES: set[Path] = set()

    ## Lifecycle

    def __init__(self, serial_device_path: Path):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        self.serial_device_path = serial_device_path

        ## Perform platform specific initialization
        self._initializer = InheritedClassPlatformOperator().get_communicator_initializer(self)
        self._initializer()

    ## Properties

    @property
    def sensor_type(self) -> SensorType:
        return SensorType.SERIAL

    ## Communicator Methods

    def initialize_communicator_raspberrypi(self):
        def get_serial_hardware_state() -> bool:
            """Is the serial hardware enabled or disabled?"""

            return_value = int(os.system("raspi-config nonint get_serial_hw"))
            return (return_value == 0)


        def validate_serial_device_path(serial_device_path: Path) -> bool:
            """Is the provided serial device path available?"""

            return_value = int(os.system(f"[ -e {serial_device_path} ]"))
            return (return_value == 0)


        ## Verify that that the serial hardware is available
        if (not get_serial_hardware_state()):
            ## todo: Link to the docs for enabling the serial hardware
            raise IOError("Serial hardware is not enabled on this device.")

        ## Verify that the serial path exists
        if (not validate_serial_device_path(self.serial_device_path)):
            raise IOError(f"Serial path {self.serial_device_path} doesn't exist")

        ## Register the sensor, and make sure there aren't any collisions
        try:
            SerialCommunicator.register_sensor(self.serial_device_path)
            self.logger.debug(f"Registered serial sensor. Serial device path: {self.serial_device_path}")
        except DeviceInUseException as e:
            self.logger.error(f"Unable to register serial sensor, device already in use. {e}")
            return

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
