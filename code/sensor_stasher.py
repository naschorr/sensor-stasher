import asyncio
import subprocess
import platform
import uuid
import logging
from datetime import datetime, timedelta

from sensor.sensor_manager import SensorManager
from storage.storage_manager import StorageManager
from storage.storage_adapter import StorageAdapter
from storage.clients.influx.influxdb_client import InfluxDBClient
from models.config.sensor_stasher_config import SensorStasherConfig
from models.platform_type import PlatformType

from utilities.configuration import Configuration
from utilities.logging.logging import Logging
from utilities.misc import get_current_platform


class SensorStasher:
    def __init__(self):
        configuration: SensorStasherConfig = Configuration.load_configuration()
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))

        self.sensor_poll_interval_seconds = configuration.sensor_poll_interval_seconds
        self.system_type = configuration.system_type if configuration.system_type is not None else platform.platform()
        self.system_id: str = configuration.system_id if configuration.system_id is not None else self._get_system_id()

        self._loop = None
        self.sensor_manager: SensorManager = SensorManager(configuration)
        self.storage_manager: StorageManager = StorageManager(self.system_type, self.system_id)

        self.logger.debug(f"Initialized SensorStasher with system type: '{self.system_type}', system id: '{self.system_id}', and sensor poll interval: '{self.sensor_poll_interval_seconds}' seconds.")


    def _get_system_id(self) -> str:
        system_id = None

        try:
            if (get_current_platform() ==  PlatformType.WINDOWS):
                ## Thanks to https://stackoverflow.com/a/66953913/1724602
                system_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
            elif (get_current_platform() == PlatformType.RASPBERRYPI):
                ## Thanks to https://stackoverflow.com/a/37775731/1724602
                system_id = str(subprocess.check_output(['cat', '/var/lib/dbus/machine-id']), 'utf-8').strip()
        except Exception as e:
            self.logger.error(f"Error during retrieval of system id: {e}")

        if (system_id is None or len(system_id) == 0):
            self.logger.warn("Unable to retrieve system id, using system's MAC address as fallback. Note that this may not be static or unique.")
            system_id = str(uuid.getnode())

        return system_id


    def register_storage(self, storage: StorageAdapter):
        self.storage_manager.register_storage(storage)


    async def _process_sensor_data_loop(self):
        while (True):
            sensor_data = await self.sensor_manager.accumulate_all_sensor_data()
            active_sensor_ids = {sensor_datum.metadata['sensor_id']: sensor_datum for sensor_datum in sensor_data}
            self.logger.debug(
                f"Retrieved {len(sensor_data)} data point{'s' if len(sensor_data) != 1 else ''} from " +
                f"{len(active_sensor_ids)} sensor{'s' if len(active_sensor_ids) != 1 else ''}."
            )

            self.storage_manager.store(sensor_data)
            self.logger.debug(
                f"Stored {len(sensor_data)} data point{'s' if len(sensor_data) != 1 else ''} inside " +
                f"{self.storage_manager.storage.storage_type}."
            )

            ## DEBUG level has more detailed info, but offer up a simplified version for less intense log levels
            if (self.logger.level == logging.INFO):
                self.logger.info(
                    f"Retrieved and stored {len(sensor_data)} data point{'s' if len(sensor_data) != 1 else ''} " +
                    f"from {len(active_sensor_ids)} sensor{'s' if len(active_sensor_ids) != 1 else ''} " +
                    f"inside {self.storage_manager.storage.storage_type}. " +
                    f"Will now sleep for {self.sensor_poll_interval_seconds} seconds."
                )

            self.logger.debug(
                f"Sleeping for {self.sensor_poll_interval_seconds} seconds, next poll starts at: " +
                f"{datetime.now() + timedelta(seconds=self.sensor_poll_interval_seconds)}"
            )
            await asyncio.sleep(self.sensor_poll_interval_seconds)


    def start_monitoring(self):
        ## One event loop at a time
        if (self._loop is not None):
            self.stop_monitoring()

        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._process_sensor_data_loop())


    def stop_monitoring(self):
        ## Make sure we've got an event loop to stop
        if (self._loop is not None):
            self._loop.stop()
            self._loop.close()
            self._loop = None


if (__name__ == '__main__'):
    monitor = SensorStasher()
    monitor.register_storage(InfluxDBClient)
    monitor.start_monitoring()
