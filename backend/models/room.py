import uuid
from models import User

class Room():
    def __init__(self, room_id: uuid, name: str, capacity: int, owner=None, whitelist=None):
        self.room_id = room_id
        self.name = name
        self.capacity = capacity
        self.users = []
        self.owner=owner
        self.whitelist = whitelist if whitelist is not None else []
        
    def to_dict(self):
        return {
            "room_id": self.room_id,
            "name": self.name,
            "capacity": self.capacity,
            "owner": self.owner,
            "users": [user.to_dict() for user in self.users],
            "whitelist": [user.to_dict() for user in self.whitelist] if self.whitelist is not None else ""
        }
    
    @classmethod
    def from_dict(cls, data):
        room = cls(
            room_id=data["room_id"],
            name=data["name"],
            capacity=data["capacity"],
            owner=data.get("owner"),
            whitelist=[],
        )
        return room


    def add_user(self, user: User):
        if len(self.users) < self.capacity:
            self.users.append(user)
            return True
        return False
    
    def remove_user(self, user:User):
        self.users.remove(user)

    def add_user_to_whitelist(self, user: User):
        if user not in self.whitelist:
            self.whitelist.append(user)
            return True
        return False

    def change_owner(self, new_owner: User):
        self.owner = new_owner

    def change_capacity(self, new_capacity: int):
        if new_capacity < len(self.users):
            return False
        if new_capacity <= 0:
            return False
        
        self.capacity = new_capacity

    def equals(self, other):
        return self.room_id == other.room_id
    
    def has_capacity(self) -> bool:
        return len(self.users) >= self.capacity