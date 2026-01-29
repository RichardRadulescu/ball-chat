from __future__ import annotations
from models import Event, User, Room
from typing import TYPE_CHECKING
import uuid 
import datetime

if TYPE_CHECKING:
    from services.eventManager import EventManager
    from services.dataManager import DataManager



class EventMessage(Event):
    def __init__(self, id:uuid, user: User, room: Room, message: str, date: datetime):
        super().__init__(id, "MessageRoom", date)
        self.user= user
        self.room= room
        self.message= message
        self.datetime= date

    
    async def resolve(self):
        db = DataManager()

    
    @staticmethod
    def parse_data(data: dict) -> EventMessage:
        """
        {
            "user_id": string,
            "room_id": string
            "message": string
            "datetime": string
        }
        """
        required = {"user_id", "room_id", "datetime", "message"}
        if not required.issubset(data):
            raise ValueError("Invalid data format")
        db = DataManager()
        
        user= db.get_user_by_id(data["user_id"])
        room= db.get_room_by_id(data["room_id"])
        
        date = datetime.fromisoformat(data["datetime"])
        return EventMessage(uuid.uuid4(),user, room, data["message"], date)