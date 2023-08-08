import logging
import os
from pathlib import Path
import contextlib

from sensor.sensor_adapter import SensorAdapter
from sensor.exceptions.device_in_use_exception import DeviceInUseException
from utilities import initialize_logging, validate_system


class OneWireSensor(SensorAdapter):
    ## Statics

    ## Keep track of all in use 1-wire device paths to avoid collisions later on
    REGISTERED_ONEWIRE_DEVICES: set[Path] = set()

    ## Lifecycle

    def __init__(self, onewire_device_path: Path):
        self.logger = initialize_logging(logging.getLogger(__name__))

        ## Verify that 1-wire is available
        if (not self.get_onewire_state()):
            ## todo: Link to the docs for enabling 1-wire
            raise IOError("1-wire is not enabled on this device.")

        ## Verify that the 1-wire device is available
        if (not self.validate_onewire_device_path(onewire_device_path)):
            raise IOError(f"1-wire device path at {onewire_device_path} doesn't exist")

        ## Register the sensor, and make sure there aren't any collisions
        try:
            OneWireSensor.register_sensor(onewire_device_path)
            self.logger.debug(f"Registered 1-wire sensor. 1-wire device path: {onewire_device_path}")
        except DeviceInUseException as e:
            self.logger.error(f"Unable to register 1-wire sensor, device already in use. {e}")
            return

        ## Load the 1-wire kernel module (for GPIO)
        ## Note that you may need to load additional modules in specific drivers (ex: w1-therm for the DS18B20
        ## temperature sensor)
        os.system("modprobe w1-gpio")

    ## Methods

    @validate_system
    def get_onewire_state(self) -> bool:
        """Is the 1-wire module enabled or disabled?"""

        return_value = int(os.system("raspi-config nonint get_onewire"))
        return (return_value == 0)


    @validate_system
    def validate_onewire_device_path(self, onewire_device_path: Path) -> bool:
        """Is the provided 1-wire device path available?"""

        return_value = int(os.system(f"[ -e {onewire_device_path} ]"))
        return (return_value == 0)


    @staticmethod
    def register_sensor(serial_device_path: Path):
        if (serial_device_path in OneWireSensor.REGISTERED_ONEWIRE_DEVICES):
            raise DeviceInUseException(f"Serial device {serial_device_path} is already in use by another sensor.")

        OneWireSensor.REGISTERED_ONEWIRE_DEVICES.add(serial_device_path)


    @staticmethod
    def unregister_sensor(serial_device_path: Path):
        with contextlib.suppress(KeyError):
            OneWireSensor.REGISTERED_ONEWIRE_DEVICES.remove(serial_device_path)
