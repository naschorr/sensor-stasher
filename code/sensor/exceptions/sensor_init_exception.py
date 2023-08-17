from sensor.exceptions.sensor_exception import SensorException


class SensorInitException(SensorException):
    '''
    Exception that's thrown when a sensor fails to initialize
    '''

    def __init__(self, message: str):
        super().__init__(message)
