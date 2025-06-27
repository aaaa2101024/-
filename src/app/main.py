import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import redis.asyncio as redis
from schemas.attendance import AttendanceResponse
from api import attendance as api_attendance
from crud import attendance as crud_attendance
from database import engine, SessionLocal
from models import attendance as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
manager = ConnectionManager()

REDIS_CHANNEL = "attendance_channel"

async def redis_listener(manager: ConnectionManager):
    r = redis.from_url("redis://localhost")
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(REDIS_CHANNEL)
        print("Subscribed to channel: and listening for updates…")
        
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                print(f"Received message: {message['data']}")
                
                db = SessionLocal()
                latest_data_orm = crud_attendance.get_all_attendance()
                response = [AttendanceResponse.model_validate(item).model_dump() for item in latest_data_orm]
                await manager.broadcast(json.dumps(response, default=str))

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_listener(manager))

@app.websocket("/ws/attendance")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("A client has disconnected.")

app.include_router(api_attendance.router)