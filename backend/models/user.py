import uuid

class User():
    def __init__(self, user_id: uuid, name: str, status: str, alias=None):
        self.user_id = user_id
        self.name = name
        self.alias = alias
        self.status = status

    def to_dict(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "alias": self.alias,
            "status": self.status
        }
    
    def equals(self, other):
        return self.user_id == other.user_id