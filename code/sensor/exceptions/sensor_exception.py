class SensorException(Exception):
    '''
    Exception that's thrown when a communication device fails to be registered
    '''

    def __init__(self, message: str):
        super().__init__(message)
