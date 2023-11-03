from sensor.exceptions.sensor_exception import SensorException


class SensorMethodFinderPlatformException(SensorException):
    '''
    Exception that's thrown when the sensor method finder is unable to find a method for the current platform
    '''

    def __init__(self, message: str):
        super().__init__(message)
