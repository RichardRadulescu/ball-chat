
class UnsupportedEventError(Exception):
    """Raised when cant find error type"""
    def __init__(self, message):
        super().__init__(message)