import logging
import os
from pathlib import Path

from sensor.communicators.onewire.onewire_communicator import OneWireCommunicator
from sensor.platforms.communicators.raspberrypi_communicator import RaspberryPiCommunicator
from sensor.exceptions.device_in_use_exception import DeviceInUseException
from utilities.logging.logging import Logging


class OneWireCommunicatorRaspberryPi(OneWireCommunicator, RaspberryPiCommunicator):
    def __init__(self, onewire_device_path: Path):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        self.onewire_device_path = onewire_device_path

        ## Verify that 1-wire is available
        if (not self._get_onewire_state()):
            ## todo: Link to the docs for enabling 1-wire
            raise IOError("1-wire is not enabled on this device.")

        ## Verify that the 1-wire device is available
        if (not self._validate_onewire_device_path(self.onewire_device_path)):
            raise IOError(f"1-wire device path at {self.onewire_device_path} doesn't exist")

        ## Register the sensor, and make sure there aren't any collisions
        try:
            OneWireCommunicator.register_sensor(self.onewire_device_path)
            self.logger.debug(f"Registered 1-wire sensor. 1-wire device path: {self.onewire_device_path}")
        except DeviceInUseException as e:
            self.logger.error(f"Unable to register 1-wire sensor, device already in use. {e}")
            raise e

        ## Load the 1-wire kernel module (for GPIO)
        ## Note that you may need to load additional modules in specific drivers (ex: w1-therm for the DS18B20
        ## temperature sensor)
        os.system("modprobe w1-gpio")

    ## Methods

    def _get_onewire_state(self) -> bool:
        """Is the 1-wire module enabled or disabled?"""

        return_value = int(os.system("raspi-config nonint get_onewire"))
        return (return_value == 0)


    def _validate_onewire_device_path(self) -> bool:
        """Is the provided 1-wire device path available?"""

        return_value = int(os.system(f"[ -e {self.onewire_device_path} ]"))
        return (return_value == 0)
