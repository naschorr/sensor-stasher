from sensor.models.data.sensor_measurement import SensorMeasurement
from sensor.models.data.data_type.data_type import DataType
from sensor.models.sensor_type import SensorType


class RNGMeasurement(SensorMeasurement):
    def __init__(self, sensor_type: SensorType, sensor_id: str, number: float):
        super().__init__(DataType.TEST, sensor_type, sensor_id)

        self.number = number
