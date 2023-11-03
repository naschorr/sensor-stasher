from sensor.exceptions.sensor_exception import SensorException


class SensorReadException(SensorException):
    '''
    Exception that's thrown when a device is already in use, and cannot be registered
    '''

    def __init__(self, message: str):
        super().__init__(message)
