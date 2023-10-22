from typing import List

from sensor.models.data.sensor_datum import SensorDatum
from storage.storage_adapter import StorageAdapter

class StorageManager:
    def __init__(self, system_type: str, system_id: str):
        self.system_type = system_type
        self.system_id = system_id

        ## todo: Allow registering multiple storage adapters at once?
        self.storage: StorageAdapter = None


    def register_storage(self, storage: StorageAdapter):
        self.storage = storage


    def store(self, data: List[SensorDatum]):
        ## Can't store data without a place to store it
        if (self.storage is None):
            raise RuntimeError("No storage adapter registered")
        
        ## No data to store? No worries, just skip this iteration
        if (not data):
            return

        self.storage.store(data)
