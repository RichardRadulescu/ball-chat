from services.connectionManager import ConnectionManager
from services.dataManager import DataManager
from models import Event, EventMessage, EventJoin, EventLeave
from utils.singleton import Singleton
from errors import UnsupportedEventError, RoomFullException
from fastapi import WebSocket

class EventManager(metaclass=Singleton):
    def __init__(self):
        self.event_map = {
            "JoinRoom": EventJoin,
            "LeaveRoom": EventLeave,
            "SendMessage": EventMessage,
        }

    async def handle_event(self, data: dict, websocket: WebSocket):
        try:
            event_type = data.get("event_type")
            event_class = self.event_map.get(event_type)
            
            if not event_class:
                raise UnsupportedEventError(f"Unknown event: {event_type}")

            # Instantiate and run
            event_obj = event_class.parse_data(data, DataManager())
            await event_obj.resolve()
            
            # Success response
            await websocket.send_json({"type": "success", "event": event_type})

        except RoomFullException as e:
            # Catching your custom error
            await websocket.send_json({
                "type": "error",
                "message": str(e),
                "code": e.code
            })

        except Exception as e:
            # The "Catch-All" for things we didn't expect (Database down, etc.)
            print(f"Critical Failure: {e}")
            await websocket.send_json({
                "type": "server_error",
                "message": "Something went wrong on our end."
            })
            