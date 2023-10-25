import asyncio
import logging
from datetime import datetime, timedelta

from common.implementation_instantiator import ImplementationInstantiator
from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.sensor_manager import SensorManager
from sensor.sensor_discoverer import SensorDiscoverer
from storage.storage_manager import StorageManager
from storage.storage_discoverer import StorageDiscoverer
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

        self.logger.debug(f"Initialized SensorStasher with system type: '{configuration.system_type}', system id: '{configuration.system_id}', and sensor poll interval: '{self.sensor_poll_interval_seconds}' seconds.")


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
