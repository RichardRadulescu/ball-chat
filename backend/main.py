from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from typing import List
from services.connectionManager import ConnectionManager
from services.eventManager import EventManager
from services.dataManager import DataManager
from models.user import User
from uuid import uuid4
import random

@asynccontextmanager
async def lifespan(app: FastAPI):
    connectionManager= ConnectionManager()
    dataManager= DataManager()
    eventManager= EventManager()
    app.state.connectionManager = connectionManager
    app.state.dataManager = dataManager
    app.state.eventManager = eventManager
    yield 

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("../frontend/index.html")

@app.get("/rooms")
async def get_rooms():
    return DataManager().rooms

@app.get("/users")
async def get_rooms():
    return DataManager().users

@app.get("/users/create")
async def create_user():
    adjectives = ["Speedy", "Lazy", "Mystic", "Crimson", "Golden", "Silent"]
    nouns = ["Panda", "Wizard", "Falcon", "Ghost", "Knight", "Otter"]
    user = User(uuid4(), f"{random.choice(adjectives)} {random.choice(nouns)}" ,"online")
    db=DataManager()
    db.users[str(user.user_id)]=user
    db.update_user()
    return user

# --- 2. The Chat Entry Point ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    conn_manager = websocket.app.state.connectionManager
    event_handler = websocket.app.state.eventManager

    await conn_manager.subscribe(websocket)
    try:
        while True:
            # 1. Receive JSON instead of raw text
            data = await websocket.receive_json() 
            print(data)
            # 2. Let the Event Manager handle the logic
            # This identifies if it's a "SendMessage", "LeaveRoom", etc.
            await event_handler.handle_event(data, websocket)
            
    except WebSocketDisconnect:
        conn_manager.unsubscribe(websocket)
