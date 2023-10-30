from sensor.models.data.sensor_measurement import SensorMeasurement
from sensor.models.data.data_type.data_type import DataType


class RNGMeasurement(SensorMeasurement):
    def __init__(self, sensor_name: str, sensor_id: str, number: float):
        super().__init__(DataType.SCALAR, sensor_name, sensor_id)

        self.number = number
