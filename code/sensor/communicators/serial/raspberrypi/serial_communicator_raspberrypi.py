import os
from pathlib import Path

from sensor.communicators.serial.serial_communicator import SerialCommunicator
from sensor.platforms.communicators.raspberrypi_communicator import RaspberryPiCommunicator
from sensor.exceptions.device_in_use_exception import DeviceInUseException
from utilities.logging.logging import Logging


class SerialCommunicatorRaspberryPi(SerialCommunicator, RaspberryPiCommunicator):
    def __init__(self, serial_device_path: Path):
        self.logger = Logging.LOGGER

        self.serial_device_path = serial_device_path

        ## Verify that that the serial hardware is available
        if (not self._get_serial_hardware_state()):
            ## todo: Link to the docs for enabling the serial hardware
            raise IOError("Serial hardware is not enabled on this device.")

        ## Verify that the serial path exists
        if (not self._validate_serial_device_path()):
            raise IOError(f"Serial path {self.serial_device_path} doesn't exist")

        ## Register the sensor, and make sure there aren't any collisions
        try:
            SerialCommunicator.register_sensor(self.serial_device_path)
            self.logger.debug(f"Registered serial sensor. Serial device path: {self.serial_device_path}")
        except DeviceInUseException as e:
            self.logger.error(f"Unable to register serial sensor, device already in use. {e}")
            raise e

    ## Methods

    def _get_serial_hardware_state(self) -> bool:
        """Is the serial hardware enabled or disabled?"""

        return_value = int(os.system("raspi-config nonint get_serial_hw"))
        return (return_value == 0)


    def _validate_serial_device_path(self) -> bool:
        """Is the provided serial device path available?"""

        return_value = int(os.system(f"[ -e {self.serial_device_path} ]"))
        return (return_value == 0)
