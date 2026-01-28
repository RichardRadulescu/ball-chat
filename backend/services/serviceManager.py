from services.dataManager import DataManager
from services.eventManager import EventManager
from services.connectionManager import ConnectionManager


class ServiceManager():
    def __init__(self):
        pass

    async def startup(self):
        self.connection_manager = ConnectionManager()
        self.data_manager = DataManager()
        self.event_manager = EventManager(self.connection_manager, self.data_manager)

    def get_connection_manager(self) -> ConnectionManager:
        return self.connection_manager
    
    def get_data_manager(self) -> DataManager:
        return self.data_manager
    
    def get_event_manager(self) -> EventManager:
        return self.event_manager