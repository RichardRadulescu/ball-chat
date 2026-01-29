# Source - https://stackoverflow.com/a
# Posted by agf, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-29, License - CC BY-SA 4.0
import threading

class Singleton(type):
    _instances={}
    _lock = threading.Lock()  # Added a lock object

    def __call__(cls, *args, **kwargs):
        with cls._lock:  # Ensure only one thread can check/create at a time
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]