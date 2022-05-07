import datetime
from typing import Dict

from sensor.sensor_categories import SensorCategories


class SensorDatum:
    def __init__(self, sensor_category: SensorCategories, sensor_type: str, sensor_id: str):
        self.metadata = {
            "sensor_category": sensor_category.value,
            "sensor_type": sensor_type,
            "sensor_id": sensor_id,
            "timestamp": datetime.datetime.now().isoformat()
        }


    def __str__(self) -> str:
        return str(self.to_dict())


    def to_dict(self) -> Dict:
        output = self.__dict__
        ## Don't expose the metadata in the output dict to be stored in the database
        del output["metadata"]

        return output
