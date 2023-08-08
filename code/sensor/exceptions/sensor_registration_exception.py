from sensor.exceptions.sensor_exception import SensorException


class SensorRegistrationException(SensorException):
    '''
    Exception that's thrown when a communication device fails to be registered
    '''

    def __init__(self, message: str):
        super().__init__(message)
