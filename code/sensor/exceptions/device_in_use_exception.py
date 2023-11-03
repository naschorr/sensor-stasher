from sensor.exceptions.sensor_registration_exception import SensorRegistrationException


class DeviceInUseException(SensorRegistrationException):
    '''
    Exception that's thrown when a device is already in use, and cannot be registered
    '''

    def __init__(self, message: str):
        super().__init__(message)
