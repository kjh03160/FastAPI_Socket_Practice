from fastapi import WebSocket
from app import schemas
import json
import pickle

from app.utils import modules

redis = modules.redis

# TODO: Change the structure for distributed server(worker) -> use redis brocker
class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        if self.connections.get(room_id):
            self.connections[room_id].append(websocket)
        else:
            self.connections[room_id] = [websocket]

    # async def broadcast(self, data: str):
    #     for connection in self.connections:
    #         await connection.send_text(data)
    
    # TODO: Consider room and message structure
    async def send_message(self, mine: WebSocket, data: schemas.MessageCreateSchema):
        sockets = self.connections[data['room_id']]
        # data['sender_id'], data['receiver']
        for s in sockets:
            if s != mine:
                await s.send_json(data)
                
    async def disconnect(self, websocket: WebSocket, room_id: int):
        sockets = self.connections[room_id]
        sockets.remove(websocket)
        

manager = ConnectionManager()