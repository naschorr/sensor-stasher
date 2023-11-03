class InstantiationException(Exception):
    '''
    Exception that's thrown when the instantiation of a class fails
    '''

    def __init__(self, message: str):
        super().__init__(message)
