from abc import ABC, abstractmethod
import uuid
import { connectionManager } from '../services/connectionManager.py'

class Event(ABC):
    def __init__(self, id: uuid, eventType: str, date):
        self.id = id
        self.eventType = eventType
        self.date = date


    @abstractmethod
    async def resolve(self, manager: , db):
        """Each event must implement how it 'resolves' itself"""
        pass

    @staticmethod
    @abstractmethod
    def parse_data(data: dict) -> bool:
        """Each event must implement how to parse its data from a dict"""
        pass

# join Room, leave Room, message sent, friend request, unfriend, status update