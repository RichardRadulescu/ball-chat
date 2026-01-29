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
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a User instance from a dictionary.
        Uses .get() for alias to handle cases where it might be missing.
        """
        return cls(
            user_id=data.get("user_id") or data.get("id"), # Handles both naming styles
            name=data.get("name"),
            status=data.get("status"),
            alias=data.get("alias")
        )