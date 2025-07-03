from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from api import attendance
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# try :
#     with sqlite3.connect('../data/testDB.db') as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
    
#         cursor.execute("SELECT * FROM attendance")
#         rows_from_db = cursor.fetchall()

# except sqlite3.Error as e:
#     print(f"データベースエラー: {e}")
#     rows_from_db = []

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

app = FastAPI()

origins = [
    "http://localhost:5173",   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"], 
)

app.include_router(attendance.router)

@app.post("/notify-update")
async def notify_update():
    await manager.broadcast("database_updated")
    return {"message": "Notification sent to all clients."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

