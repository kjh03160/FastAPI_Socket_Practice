from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.connections[client_id] = websocket
        # redis.setex(client_id, 3600, json.dumps({"socket": websocket}))

    # async def broadcast(self, data: str):
    #     for connection in self.connections:
    #         await connection.send_text(data)
    async def send_message(self, data: str, to: int):
        socket = self.connections[to]
        await socket.send_text(data)

manager = ConnectionManager()