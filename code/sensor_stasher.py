import asyncio
import os
import subprocess
import platform
import uuid
import logging
from pathlib import Path

from sensor.sensor_manager import SensorManager
from sensor.sensor_adapter import SensorAdapter
from sensor.sensors.pms7003.pms7003_driver import PMS7003Driver
from sensor.sensors.test_sensor.test_sensor_driver import TestSensorDriver

from storage.storage_manager import StorageManager
from storage.storage_adapter import StorageAdapter
from storage.clients.influx.influxdb_client import InfluxDBClient
from utilities import load_config, initialize_logging

class SensorStasher:
    def __init__(self):
        config = load_config()
        self.logger = initialize_logging(logging.getLogger(__name__))

        self.sensor_poll_interval_seconds: int = config.get('sensor_poll_interval_seconds')
        system_type = config.get('system_type')
        self.system_type: str = system_type if system_type is not None else platform.platform()
        system_id = config.get('system_id')
        self.system_id: str = system_id if system_id is not None else self._get_system_id()

        self._loop = None
        self.sensor_manager: SensorManager = SensorManager()
        self.storage_manager: StorageManager = StorageManager(self.system_type, self.system_id)

        self.logger.debug(f"Initialized SensorStasher with system type: '{self.system_type}', system id: '{self.system_id}', and sensor poll interval: '{self.sensor_poll_interval_seconds}' seconds.")


    def _get_system_id(self):
        if ('nt' in os.name):
            ## Thanks to https://stackoverflow.com/a/66953913/1724602
            return str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        else:
            ## Thanks to https://stackoverflow.com/a/41569262/1724602
            return str(uuid.getnode())


    def register_sensor(self, sensor: SensorAdapter, sensor_id: str):
        self.sensor_manager.register_sensor(sensor, sensor_id)


    def register_storage(self, storage: StorageAdapter):
        self.storage_manager.register_storage(storage)


    async def _process_sensor_data_loop(self):
        while (True):
            self.logger.info("Starting sensor data processing loop")
            sensor_data = await self.sensor_manager.accumulate_all_sensor_data()
            self.logger.debug(f"Retrieved data from {len(sensor_data)} sensor{'s' if len(sensor_data) != 1 else ''}.")

            self.storage_manager.store(sensor_data)
            self.logger.debug(f"Stored data from {len(sensor_data)} sensor{'s' if len(sensor_data) != 1 else ''}.")

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
    # monitor.register_sensor(PMS7003Driver, None)
    monitor.register_sensor(TestSensorDriver, 'test_sensor_0')
    monitor.register_sensor(TestSensorDriver, 'test_sensor_1')
    monitor.register_sensor(TestSensorDriver, 'test_sensor_2')
    monitor.register_sensor(TestSensorDriver, 'test_sensor_3')
    monitor.register_sensor(TestSensorDriver, 'test_sensor_4')
    monitor.register_storage(InfluxDBClient)
    monitor.start_monitoring()
