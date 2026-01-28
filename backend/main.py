from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from typing import List
from services.serviceManager import ServiceManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    service_manager = ServiceManager()
    await service_manager.startup()

    yield {"service_manager": service_manager}

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("../frontend/index.html")

# --- 2. The Chat Entry Point ---
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    manager= websocket.app.state.service_manager.get_connection_manager()

    await manager.connect(websocket)
    try:
        await manager.broadcast(f"Client {client_id} joined the room")
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left the chat")

# --- 3. Serving the Frontend (Optional but Helpful) ---
# This allows you to visit http://localhost:8000 to see your UI
# app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")