import datetime

from sensor.models.data.data_type.data_type import DataType


class SensorDatum:
    def __init__(self, category: DataType, sensor_type: str, sensor_id: str):
        self.metadata = {
            "sensor_type": sensor_type,
            "sensor_id": sensor_id,
            "category": category.value,
            "timestamp": datetime.datetime.now().isoformat()
        }


    def __str__(self) -> str:
        return str(self.__dict__)


    def to_dict(self) -> dict:
        output = self.__dict__.copy()
        ## Don't expose the metadata in the output dict to be stored in the database
        del output["metadata"]

        return output
