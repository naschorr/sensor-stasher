import logging
import os
import contextlib

from sensor.models.sensor_type import SensorType
from sensor.models.communicator_adapter import CommunicatorAdapter
from sensor.platforms.communicators.raspberrypi_communicator import RaspberryPiCommunicator
from models.platform_type import PlatformType
from sensor.exceptions.device_in_use_exception import DeviceInUseException
from utilities.logging.logging import Logging
from utilities.utilities import get_current_platform

if (get_current_platform() == PlatformType.RASPBERRYPI):
    import smbus2   # type: ignore


class I2CCommunicator(CommunicatorAdapter, RaspberryPiCommunicator):
    ## Statics

    ## Keep track of all in use i2c devices to avoid collisions later on
    REGISTERED_I2C_DEVICES: dict[int, list[int]] = {}

    ## Lifecycle

    def __init__(self, i2c_bus: int, i2c_address: int):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address

    ## Properties

    @property
    def sensor_type(self) -> SensorType:
        return SensorType.I2C

    ## Communicator Methods

    def initialize_communicator_raspberrypi(self):
        def get_i2c_state() -> bool:
            """Is the i2c module enabled or disabled?"""

            return_value = int(os.system("raspi-config nonint get_i2c"))
            return (return_value == 0)


        def validate_i2c_bus(i2c_bus: int) -> bool:
            """Is the provided i2c bus available?"""

            return_value = int(os.system(f"i2cdetect -y {i2c_bus}"))
            return (return_value == 0)


        ## Verify that i2c is available
        if (not get_i2c_state()):
            ## todo: Link to the docs for enabling i2c
            raise IOError("i2c is not enabled on this device.")

        ## Verify that the i2c bus is available
        if (not validate_i2c_bus(self.i2c_bus)):
            raise IOError(f"i2c bus {self.i2c_bus} is not available.")

        ## todo: verify that i2c address is in range?

        ## Register the sensor, and make sure there aren't any collisions
        try:
            I2CCommunicator.register_sensor(self.i2c_bus, self.i2c_address)
            self.logger.debug(f"Registered i2c sensor. i2c_bus: {self.i2c_bus}, i2c_address: {self.i2c_address}")
        except DeviceInUseException as e:
            self.logger.error(f"Unable to register i2c sensor, device already in use. {e}")
            return

        self.bus = smbus2.SMBus(self.i2c_bus)

    ## Methods

    @staticmethod
    def register_sensor(i2c_bus: int, i2c_address: int):
        ## Is the bus not in use?
        if (i2c_bus not in I2CCommunicator.REGISTERED_I2C_DEVICES):
            I2CCommunicator.REGISTERED_I2C_DEVICES[i2c_bus] = [i2c_address]
        ## Is the bus in use, but not the address?
        elif (i2c_address not in I2CCommunicator.REGISTERED_I2C_DEVICES[i2c_bus]):
            I2CCommunicator.REGISTERED_I2C_DEVICES[i2c_bus].append(i2c_address)
        ## Is the bus and address in use?
        else:
            raise DeviceInUseException(f"i2c bus {i2c_bus} and address {i2c_address} are already in use by another sensor.")


    @staticmethod
    def unregister_sensor(i2c_bus: int, i2c_address: int):
        with contextlib.suppress(ValueError):
            I2CCommunicator.REGISTERED_I2C_DEVICES.get(i2c_bus, []).remove(i2c_address)
