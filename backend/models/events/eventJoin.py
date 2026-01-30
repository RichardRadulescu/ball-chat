from __future__ import annotations
from models import Event, User, Room
from errors import RoomFullException
from typing import TYPE_CHECKING
import uuid 
from datetime import datetime

if TYPE_CHECKING:
    from services.eventManager import EventManager
    from services.dataManager import DataManager



class EventJoin(Event):
    def __init__(self, id:uuid, user: User, room: Room,  date: datetime):
        super().__init__(id, "JoinRoom", date)
        self.user= user
        self.room= room
        self.datetime= date

    
    async def resolve(self, db: DataManager):
        # Can make it so it uses alias and check for uniqueness. So i dont expose ids
        if not self.room.has_capacity():
            raise RoomFullException("Can not join. Room is full.")
        
        db.add_user_to_room(self.room.room_id, self.user.user_id)

        return ", ".join(user.name for user in self.room.users)

    async def get_broadcast_message(self) -> None | str:
        return f"User {self.user.name} has joined."
    
    @staticmethod
    def parse_data(data: dict, db: DataManager) -> EventJoin:
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

        
        date = datetime.fromisoformat(data["datetime"].replace("Z", "+00:00"))#for python 3.9
        
        return EventJoin(uuid.uuid4(),user, room, date)