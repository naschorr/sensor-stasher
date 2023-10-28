import logging
import os

import smbus2   # type: ignore

from sensor.communicators.i2c.i2c_communicator import I2CCommunicator
from sensor.platforms.communicators.raspberrypi_communicator import RaspberryPiCommunicator
from sensor.exceptions.device_in_use_exception import DeviceInUseException
from utilities.logging.logging import Logging


class I2CCommunicatorRaspberryPi(I2CCommunicator, RaspberryPiCommunicator):
    def __init__(self, i2c_bus: int, i2c_address: int):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address

        ## Verify that i2c is available
        if (not self._get_i2c_state()):
            ## todo: Link to the docs for enabling i2c
            raise IOError("i2c is not enabled on this device.")

        ## Verify that the i2c bus is available
        if (not self._validate_i2c_bus()):
            raise IOError(f"i2c bus {self.i2c_bus} is not available.")

        ## todo: verify that i2c address is in range?

        ## Register the sensor, and make sure there aren't any collisions
        try:
            I2CCommunicator.register_sensor(self.i2c_bus, self.i2c_address)
            self.logger.debug(f"Registered i2c sensor. i2c_bus: {self.i2c_bus}, i2c_address: {self.i2c_address}")
        except DeviceInUseException as e:
            self.logger.error(f"Unable to register i2c sensor, device already in use. {e}")
            raise e

        self.bus = smbus2.SMBus(self.i2c_bus)

    ## Methods

    def _get_i2c_state(self) -> bool:
        """Is the i2c module enabled or disabled?"""

        return_value = int(os.system("raspi-config nonint get_i2c"))
        return (return_value == 0)


    def _validate_i2c_bus(self) -> bool:
        """Is the provided i2c bus available?"""

        return_value = int(os.system(f"i2cdetect -y {self.i2c_bus}"))
        return (return_value == 0)
