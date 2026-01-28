from .connectionManager import ConnectionManager
from .dataManager import DataManager
from ..models.event import Event

class EventManager():
    def __init__(self, pub_sub: ConnectionManager, db: DataManager):
        self.pub_sub = pub_sub
        self.db = db

    async def handle_event(self, event: Event):
        await event.resolve(self, self.pub_sub, self.db)