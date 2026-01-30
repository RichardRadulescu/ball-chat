from __future__ import annotations
from models import Event, User, Room
from typing import TYPE_CHECKING
import uuid 
from datetime import datetime

if TYPE_CHECKING:
    from services.eventManager import EventManager
    from services.dataManager import DataManager



class EventLeave(Event):
    def __init__(self, id:uuid, user: User, room: Room,  date: datetime):
        super().__init__(id, "LeaveRoom", date)
        self.user= user
        self.room= room
        self.datetime= date

    
    async def resolve(self, db: DataManager):
        
        self.room.remove_user(self.user)
        db.update_room(self.room)

    def get_broadcast_message(self):
        return f"User {self.user.name} has left the room."
    
    @staticmethod
    def parse_data(data: dict, db: DataManager) -> EventLeave:
        """
        {
            "user_id": string,
            "room_id": string
            "datetime": string
        }
        """
        required = {"user_id", "room_id", "datetime"}
        if not required.issubset(data):
            raise ValueError("Invalid data format")
        
        user= db.get_user_by_id(data["user_id"])
        room= db.get_room_by_id(data["room_id"])
        date = datetime.fromisoformat(data["datetime"])
        return EventLeave(uuid.uuid4(),user, room, date)