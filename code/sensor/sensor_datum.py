import datetime
from typing import Dict

from sensor.datum_category import DatumCategory


class SensorDatum:
    def __init__(self, category: DatumCategory, sensor_type: str, sensor_id: str):
        self.metadata = {
            "sensor_type": sensor_type,
            "sensor_id": sensor_id,
            "category": category.value,
            "timestamp": datetime.datetime.now().isoformat()
        }


    def __str__(self) -> str:
        return str(self.__dict__)


    def to_dict(self) -> Dict:
        output = self.__dict__.copy()
        ## Don't expose the metadata in the output dict to be stored in the database
        del output["metadata"]

        return output
