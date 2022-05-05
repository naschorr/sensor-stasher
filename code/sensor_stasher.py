import asyncio
from typing import Dict

from sensor.sensor_adapter import SensorAdapter
from sensor.sensors.pms7003.pms7003_driver import PMS7003Driver
from sensor.sensors.test_sensor.test_sensor_driver import TestSensorDriver
from sensor.sensor_manager import SensorManager


class SensorStasher:
    def __init__(self, bucket_name: str, poll_interval_seconds: int):
        self.bucket_name: str = bucket_name
        self.poll_interval_seconds: int = poll_interval_seconds

        self.sensor_manager: SensorManager = SensorManager()

        self._loop = None


    def register_sensor(self, sensor: SensorAdapter, config: Dict = None):
        if config is None:
            config = {}

        self.sensor_manager.register_sensor(sensor, config)


    async def _process_sensor_data_loop(self):
        while (True):
            sensor_data = await self.sensor_manager._accumulate_all_sensor_data()
            print(sensor_data)

            await asyncio.sleep(self.poll_interval_seconds)


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
    monitor = SensorStasher("sensor_stasher", 60)
    # monitor.register_sensor(PMS7003Driver)
    monitor.register_sensor(TestSensorDriver, {'name': 'test_sensor_0'})
    monitor.register_sensor(TestSensorDriver, {'name': 'test_sensor_1'})
    monitor.register_sensor(TestSensorDriver, {'name': 'test_sensor_2'})
    monitor.register_sensor(TestSensorDriver, {'name': 'test_sensor_3'})
    monitor.register_sensor(TestSensorDriver, {'name': 'test_sensor_4'})
    monitor.start_monitoring()
