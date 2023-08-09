import logging
import os
from pathlib import Path
import contextlib

from sensor.sensor_adapter import SensorAdapter
from sensor.exceptions.device_in_use_exception import DeviceInUseException
from utilities.utilities import validate_system
from utilities.logging.logging import Logging


class SerialSensor(SensorAdapter):
    ## Statics

    ## Keep track of serial device paths that are in use to avoid collisions later on
    REGISTERED_SERIAL_DEVICES: set[Path] = set()

    ## Lifecycle

    def __init__(self, serial_device_path: Path):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        ## Verify that that the serial hardware is available
        if (not self.get_serial_hardware_state()):
            ## todo: Link to the docs for enabling the serial hardware
            raise IOError("Serial hardware is not enabled on this device.")

        ## Verify that the serial path exists
        if (not self.validate_serial_device_path(serial_device_path)):
            raise IOError(f"Serial path {serial_device_path} doesn't exist")

        ## Register the sensor, and make sure there aren't any collisions
        try:
            SerialSensor.register_sensor(serial_device_path)
            self.logger.debug(f"Registered serial sensor. Serial device path: {serial_device_path}")
        except DeviceInUseException as e:
            self.logger.error(f"Unable to register serial sensor, device already in use. {e}")
            return

    ## Methods

    @validate_system
    def get_serial_hardware_state(self) -> bool:
        """Is the serial hardware enabled or disabled?"""

        return_value = int(os.system("raspi-config nonint get_serial_hw"))
        return (return_value == 0)


    @validate_system
    def validate_serial_device_path(self, serial_device_path: Path) -> bool:
        """Is the provided serial device path available?"""

        return_value = int(os.system(f"[ -e {serial_device_path} ]"))
        return (return_value == 0)


    @staticmethod
    def register_sensor(serial_device_path: Path):
        if (serial_device_path in SerialSensor.REGISTERED_SERIAL_DEVICES):
            raise DeviceInUseException(f"Serial device {serial_device_path} is already in use by another sensor.")

        SerialSensor.REGISTERED_SERIAL_DEVICES.add(serial_device_path)


    @staticmethod
    def unregister_sensor(serial_device_path: Path):
        with contextlib.suppress(KeyError):
            SerialSensor.REGISTERED_SERIAL_DEVICES.remove(serial_device_path)
