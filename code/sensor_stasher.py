import asyncio
from datetime import datetime, timedelta

from common.implementation_instantiator import ImplementationInstantiator
from common.models.config.sensor_stasher_config import SensorStasherConfig
from sensor.sensor_manager import SensorManager
from sensor.sensor_discoverer import SensorDiscoverer
from stasher.storage_manager import StorageManager
from stasher.stasher_discoverer import StasherDiscoverer
from utilities.configuration.sensor_stasher_configuration import SensorStasherConfiguration
from utilities.configuration.configuration import Configuration
from utilities.logging.logging import Logging


class SensorStasher:
    def __init__(self):
        ## Config
        sensor_stasher_configuration = SensorStasherConfiguration().load_configuration()
        self.logger = Logging(sensor_stasher_configuration.logging).LOGGER
        sensor_discoverer = SensorDiscoverer(sensor_stasher_configuration.sensors_directory_path)
        stasher_discoverer = StasherDiscoverer()
        global_configuration = Configuration(sensor_discoverer, stasher_discoverer)
        sensors_configuration = global_configuration.sensors_configuration
        stashers_configuration = global_configuration.stasher_configuration
        implementation_instantiator = ImplementationInstantiator(self.logger, sensor_stasher_configuration)

        self.sensor_poll_interval_seconds: int = sensor_stasher_configuration.sensor_poll_interval_seconds
        self._loop = None
        self.sensor_manager: SensorManager = SensorManager(
            self.logger,
            sensor_stasher_configuration,
            sensors_configuration,
            sensor_discoverer,
            implementation_instantiator
        )
        self.storage_manager: StorageManager = StorageManager(
            self.logger,
            sensor_stasher_configuration,
            stashers_configuration,
            stasher_discoverer,
            implementation_instantiator
        )

        self.logger.debug(f"Initialized SensorStasher with system type: '{sensor_stasher_configuration.system_type}', system id: '{sensor_stasher_configuration.system_id}', and sensor poll interval: '{self.sensor_poll_interval_seconds}' seconds.")


    async def _process_sensor_measurements_loop(self):
        while (True):
            sensor_measurements = await self.sensor_manager.accumulate_all_sensor_measurements()

            if (not sensor_measurements):
                self.logger.debug("No sensor data retrieved, nothing will be stored")
            else:
                active_sensor_ids = {sensor_measurement.metadata['sensor_id']: sensor_measurement for sensor_measurement in sensor_measurements}
                self.logger.debug(
                    f"Retrieved {len(sensor_measurements)} data point{'s' if len(sensor_measurements) != 1 else ''} from " +
                    f"{len(active_sensor_ids)} sensor{'s' if len(active_sensor_ids) != 1 else ''}."
                )

                self.storage_manager.store(sensor_measurements)
                self.logger.debug(f"Stored {len(sensor_measurements)} data point{'s' if len(sensor_measurements) != 1 else ''}")

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
        self._loop.run_until_complete(self._process_sensor_measurements_loop())


    def stop_monitoring(self):
        self._loop.stop()
        self._loop.close()
        self._loop = None


if (__name__ == '__main__'):
    monitor = SensorStasher()
    monitor.start_monitoring()
