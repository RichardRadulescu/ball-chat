from utils.singleton import Singleton
from fastapi import WebSocket

class ConnectionManager(metaclass=Singleton):
    def __init__(self):
        self.connections = []

    async def subscribe(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def unsubscribe(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def publish(self, message: str):
        for websocket in list(self.connections):
            try:
                await websocket.send_text(message)
            except Exception:
                # Remove broken connections
                await self.unsubscribe(websocket)
