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

    def _load_all(self):
        # Load users
        users_json = self._load_json("users.json")
        for user_id, user_data in users_json.items():
            self.users[user_id] = User.from_dict(user_data)

        # Load rooms
        rooms_json = self._load_json("rooms.json")
        for room_id, room_data in rooms_json.items():
            room = Room.from_dict(room_data)

            # Attach user objects
            for user_id in room_data.get("users", []):
                if user_id in self.users:
                    room.users.append(self.users[user_id])

            # Attach whitelist
            for user_id in room_data.get("whitelist", []):
                if user_id in self.users:
                    room.whitelist.append(self.users[user_id])

            self.rooms[room_id] = room

    def _load_json(self, filename: str):
        path = self.data_dir / filename
        if not path.exists():
            return {}
        with open(path, "r") as f:
            return json.load(f)

    def _write_json_atomic(self, filename: str, data):
        path = self.data_dir / filename
        tmp_path = path.with_suffix(".tmp")

        with open(tmp_path, "w") as f:
            json.dump(data, f, indent=2)

        tmp_path.replace(path)


    def get_room_by_id(self, room_id):
        return self.rooms.get(room_id)


    def get_user_by_id(self, user_id):
        return self.users.get(user_id)


    def update_room(self, room):
        with self._lock:
            # Convert all rooms to dicts
            rooms_dict = {rid: r.to_dict() for rid, r in self.rooms.items()}
            self._write_json_atomic("rooms.json", rooms_dict)


    def update_user(self, user):
        with self._lock:
            users_dict = {uid: u.to_dict() for uid, u in self.users.items()}
            self._write_json_atomic("users.json", users_dict)


    def add_user_to_room(self, room_id, user_id):
        room = self.get_room_by_id(room_id)
        user = self.get_user_by_id(user_id)
        room.add_user(user)
        self.update_room(room)

    def remove_user_to_room(self, room_id, user_id):
        room = self.get_room_by_id(room_id)
        user = self.get_user_by_id(user_id)
        room.remove_user(user)
        self.update_room(room)