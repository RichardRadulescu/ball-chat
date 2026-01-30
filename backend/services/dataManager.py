import json
import threading
from pathlib import Path
from models import Room, User
from utils.singleton import Singleton

class DataManager(metaclass=Singleton):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._lock = threading.Lock()

        # In-memory stores
        self.rooms = {}
        self.users = {}

        self._load_all()


    def _load_json(self, filename: str):
        path = self.data_dir / filename
        if not path.exists():
            return {}
        with open(path, "r") as f:
            return json.load(f)
        
    
    def _load_all(self):
        # Load users
        users_json = self._load_json("users.json")
        for user_id, user_data in users_json.items():
            self.users[user_id] = User.from_dict(user_data)

        # Load rooms
        rooms_json = self._load_json("rooms.json")
        for room_id, room_data in rooms_json.items():
            room = Room.from_dict(room_data)
            
            # Reset lists to ensure we don't double-up on load
            room.users = []
            room.whitelist = []

            # Attach user objects by looking up the ID
            for raw_user in room_data.get("users", []):
                # FIX: If raw_user is a dict (messy data), get the ID. Otherwise, use it as ID.
                uid = raw_user.get("user_id") if isinstance(raw_user, dict) else raw_user
                if uid in self.users:
                    room.users.append(self.users[uid])

            for raw_user in room_data.get("whitelist", []):
                uid = raw_user.get("user_id") if isinstance(raw_user, dict) else raw_user
                if uid in self.users:
                    room.whitelist.append(self.users[uid])

            self.rooms[room_id] = room

    def update_room(self, room):
        with self._lock:
            rooms_dict = {}
            for rid, r in self.rooms.items():
                # Convert object to dict
                d = r.to_dict()
                # OVERRIDE: Replace object list with ID list for the JSON file
                d["users"] = [u.user_id for u in r.users]
                d["whitelist"] = [u.user_id for u in r.whitelist]
                rooms_dict[rid] = d
                
            self._write_json_atomic("rooms.json", rooms_dict)

    def add_user_to_room(self, room_id, user_id):
        room = self.get_room_by_id(room_id)
        user = self.get_user_by_id(user_id)
        
        if room and user:
            if not any(u.user_id == user_id for u in room.users):
                room.add_user(user)
                self.update_room(room)

    def _write_json_atomic(self, filename: str, data):
        path = self.data_dir / filename
        tmp_path = path.with_suffix(".tmp")

        with open(tmp_path, "w") as f:
            json.dump(data, f, indent=2)

        tmp_path.replace(path)

#Add exception for not found
    def get_room_by_id(self, room_id):
        return self.rooms.get(room_id)


    def get_user_by_id(self, user_id):
        return self.users.get(user_id)


    def update_user(self):
        with self._lock:
            users_dict = {uid: u.to_dict() for uid, u in self.users.items()}
            self._write_json_atomic("users.json", users_dict)


    def remove_user_to_room(self, room_id, user_id):
        room = self.get_room_by_id(room_id)
        user = self.get_user_by_id(user_id)
        
        if room and user:            
            if any(u.user_id == user_id for u in room.users):
                room.remove_user(user)
                self.update_room(room)            