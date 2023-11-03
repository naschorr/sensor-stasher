import contextlib
from abc import ABC

from sensor.models.sensor_type import SensorType
from sensor.communicators.models.registerable_communicator_adapter import RegisterableCommunicatorAdapter
from sensor.exceptions.device_in_use_exception import DeviceInUseException


class I2CCommunicator(RegisterableCommunicatorAdapter, ABC):
    ## Statics

    ## Keep track of all in use i2c devices to avoid collisions later on
    REGISTERED_I2C_DEVICES: dict[int, list[int]] = {}

    ## Properties

    @property
    def sensor_type(self) -> SensorType:
        return SensorType.I2C

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
