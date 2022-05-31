from typing import List

from sensor.sensor_datum import SensorDatum
from storage.storage_adapter import StorageAdapter

class StorageManager:
    def __init__(self, system_type: str, system_id: str):
        self.system_type = system_type
        self.system_id = system_id

        ## todo: Allow registering multiple storage adapters at once?
        self.storage: StorageAdapter = None


    def register_storage(self, storage: StorageAdapter):
        ## todo: similar sensor registration exception handling once multiple storage endpoints are supported
        self.storage = storage(self.system_type, self.system_id)


    def store(self, data: List[SensorDatum]):
        if (self.storage is None):
            raise RuntimeError("No storage adapter registered")

        self.storage.store(data)
