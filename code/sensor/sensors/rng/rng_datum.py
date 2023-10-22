from sensor.models.data.sensor_datum import SensorDatum
from sensor.models.data.data_type.data_type import DataType
from sensor.models.sensor_type import SensorType


class RNGDatum(SensorDatum):
    def __init__(self, sensor_type: SensorType, sensor_id: str, number: float):
        super().__init__(DataType.TEST, sensor_type, sensor_id)

        self.number = number
