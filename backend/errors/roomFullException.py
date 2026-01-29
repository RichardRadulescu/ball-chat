class RoomFullException(Exception):
    """Raised when a user tries to join a room that is at capacity."""
    def __init__(self, message):
        super().__init__(message)
        