import asyncio
import os
import subprocess
import platform
import uuid
import logging
from datetime import datetime, timedelta

from common.implementation_instantiator import ImplementationInstantiator
from sensor.sensor_manager import SensorManager
from sensor.models.sensor_adapter import SensorAdapter
from sensor.sensor_discoverer import SensorDiscoverer
from storage.storage_manager import StorageManager
from storage.models.storage_adapter import StorageAdapter
from storage.storage_discoverer import StorageDiscoverer
from models.config.sensor_stasher_config import SensorStasherConfig
from utilities.configuration.sensor_stasher_configuration import SensorStasherConfiguration
from utilities.configuration.configuration import Configuration
from utilities.logging.logging import Logging


class SensorStasher:
    def __init__(self):
        ## Preconfig
        sensor_stasher_configuration = SensorStasherConfiguration().load_configuration()
        logger = Logging(
            log_level = sensor_stasher_configuration.log_level,
            log_path = sensor_stasher_configuration.log_path,
            log_backup_count = sensor_stasher_configuration.log_backup_count
        )

        ## Config
        self.logger = Logging.initialize_logging(logging.getLogger(__name__))
        sensor_discoverer = SensorDiscoverer()
        storage_discoverer = StorageDiscoverer()
        global_configuration = Configuration(sensor_discoverer, storage_discoverer)
        configuration: SensorStasherConfig = global_configuration.sensor_stasher_configuration
        sensors_configuration = global_configuration.sensors_configuration
        storage_clients_configuration = global_configuration.storage_client_configuration
        implementation_instantiator = ImplementationInstantiator(logger, configuration)

        self.sensor_poll_interval_seconds: int = configuration.sensor_poll_interval_seconds
        system_type = configuration.system_type
        self.system_type: str = system_type if system_type is not None else platform.platform()
        system_id = configuration.system_id
        self.system_id: str = system_id if system_id is not None else self._get_system_id()

        self._loop = None
        self.sensor_manager: SensorManager = SensorManager(
            logger,
            configuration,
            sensors_configuration,
            sensor_discoverer,
            implementation_instantiator
        )
        self.storage_manager: StorageManager = StorageManager(
            logger,
            configuration,
            storage_clients_configuration,
            storage_discoverer,
            implementation_instantiator
        )

        self.logger.debug(f"Initialized SensorStasher with system type: '{self.system_type}', system id: '{self.system_id}', and sensor poll interval: '{self.sensor_poll_interval_seconds}' seconds.")


    def _get_system_id(self) -> str:
        ## todo: make sure this is getting sent to the storage_manager
        system_id = None

        try:
            if ('nt' in os.name):
                ## Thanks to https://stackoverflow.com/a/66953913/1724602
                system_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
            else:
                ## Thanks to https://stackoverflow.com/a/37775731/1724602
                system_id = str(subprocess.check_output(['cat', '/var/lib/dbus/machine-id']), 'utf-8').strip()
        except Exception as e:
            self.logger.error(f"Error during retrieval of system id: {e}")

        if (system_id is None or len(system_id) == 0):
            self.logger.warn("Unable to retrieve system id, using system's MAC address as fallback. Note that this may not be static or unique.")
            system_id = str(uuid.getnode())

        return system_id


    def register_sensor(self, sensor: SensorAdapter, sensor_id: str):
        self.sensor_manager.register_sensor(sensor, sensor_id)


    def register_storage(self, storage: StorageAdapter):
        self.storage_manager.register_storage(storage)


    async def _process_sensor_data_loop(self):
        while (True):
            sensor_data = await self.sensor_manager.accumulate_all_sensor_data()

            if (not sensor_data):
                self.logger.debug("No sensor data retrieved, nothing will be stored")
            else:
                active_sensor_ids = {sensor_datum.metadata['sensor_id']: sensor_datum for sensor_datum in sensor_data}
                self.logger.debug(
                    f"Retrieved {len(sensor_data)} data point{'s' if len(sensor_data) != 1 else ''} from " +
                    f"{len(active_sensor_ids)} sensor{'s' if len(active_sensor_ids) != 1 else ''}."
                )

                self.storage_manager.store(sensor_data)
                self.logger.debug(f"Stored {len(sensor_data)} data point{'s' if len(sensor_data) != 1 else ''}")

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
        self._loop.stop()
        self._loop.close()
        self._loop = None


if (__name__ == '__main__'):
    monitor = SensorStasher()
    monitor.start_monitoring()
