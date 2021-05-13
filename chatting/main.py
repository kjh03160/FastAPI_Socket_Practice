from fastapi import Depends, Path, Request, status, Response, WebSocket, \
                    BackgroundTasks, Body
from fastapi.responses import HTMLResponse
from starlette.endpoints import WebSocketEndpoint
from sqlalchemy.orm import Session

from typing import List, Dict, AsyncIterable, Optional

from app import schemas, crud, middleware, logs
from app.database import app, get_db_sess, open_database_connection_pools, close_database_connection_pools
from app.connetion_manager import manager
from app.apis import chat_room, user, message, friend
import uvicorn, json, starlette

# app.add_middleware(middleware.AuthenticationMiddleware, backend=middleware.BasicAuthBackend())
app.add_middleware(middleware.TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(middleware.CORSMiddleware, allow_headers=["*"], allow_methods=["*"])


logs.server_logger.info("-" * 10 + "Server Start" + "-" * 10 )

@app.on_event('startup')
async def startup_event():
    await open_database_connection_pools()


@app.on_event('shutdown')
async def shutdown_event():
    await close_database_connection_pools()

# @app.websocket("/ws/{room_id}")
# class MessagesEndpoint(WebSocketEndpoint):
#     async def on_connect(self, websocket):
#         await websocket.accept()
#         self.last_time = time()
#         print(f"[{self.last_time}] connected: {websocket.client}")

#     async def on_receive(self, websocket: WebSocket, data) -> None:
#         self.last_time = time()
#         print(f"[{self.last_time}] {data}")

#     async def on_disconnect(self, websocket, close_code):
#         print(f"[{time()}] disconnected: {websocket.client}")
#         print("delay:", time() - self.last_time)


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    try:
        await manager.connect(websocket, room_id)
        while True:

            data = await websocket.receive_json()
            
            # await manager.broadcast(f"Client {client_id}: {data}")
            await manager.send_message(websocket, data)
    except starlette.websockets.WebSocketDisconnect:
        # await manager.send_message(websocket, room_id)
        await manager.disconnect(websocket, room_id)
    print("end")

html = ""
with open('index.html', 'r') as f:
    html = f.read()
    

# https://bocadilloproject.github.io/guide/websockets.html#sending-messages

@app.get("/")
async def logging_check():
    server_logger = logs.server_logger
    server_logger.debug("I'm a DEBUG message")
    server_logger.info("I'm an INFO message")
    server_logger.warning("I'm a WARNING message")
    server_logger.error("I'm a ERROR message")
    server_logger.critical("I'm a CRITICAL message")

@app.get("/{id}")
async def get(request: Request, id: int):
    # print(request.user)
    return HTMLResponse(html % id)

app.include_router(message.router, prefix="/chat-room/{room_id}")
app.include_router(chat_room.router)
app.include_router(friend.router, prefix='/{user_id}/friends')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)