import logging

from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.communicators.serial.serial_communicator import SerialCommunicator
from sensor.models.sensor_adapter import SensorAdapter
from sensor.sensors.pms7003.pms7003_config import PMS7003Config
from utilities.logging.logging import Logging

class PMS7003Driver(SensorAdapter, SerialCommunicator):
    def __init__(self, sensor_stasher_configuration: SensorStasherConfig, pms7003_configuration: PMS7003Config):
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        ## Configure
        self.serial_device_path = pms7003_configuration.serial_device_path
        self.wakeup_time_seconds = pms7003_configuration.wakeup_time_seconds or 30
        self._sensor_name = pms7003_configuration.sensor_name or "PMS7003"
        self._sensor_id = pms7003_configuration.sensor_id or self.serial_device_path.name

        self.logger.debug(f"Initialized {self.sensor_type} sensor. path: '{self.serial_device_path}', id: '{self.sensor_id}', wakeup_time_seconds: '{self.wakeup_time_seconds}'")

    ## Properties

    @property
    def sensor_name(self) -> str:
        return self._sensor_name


    @property
    def sensor_id(self) -> str:
        return self._sensor_id

