from fastapi import Depends, Path, Request, status, Response, WebSocket, \
                    BackgroundTasks, Body
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from typing import List, Dict, AsyncIterable, Optional

from app.database import app, get_db_sess, open_database_connection_pools, close_database_connection_pools
from app.connetion_manager import manager
from app import schemas
from app import crud
from app.apis import chat_room, user, message

from redis import Redis
import uvicorn, json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event('startup')
async def startup_event():
    await open_database_connection_pools()


@app.on_event('shutdown')
async def shutdown_event():
    await close_database_connection_pools()

redis = Redis.from_url('redis://localhost:6379')


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    while True:
        data = await websocket.receive_text()
        to, data = data.split(',')
        # await manager.broadcast(f"Client {client_id}: {data}")
        await manager.send_message(f"to Client {client_id}: {data}", int(to))
    print("end")

# html = ""
# with open('index.html', 'r') as f:
#     html = f.read()



# https://bocadilloproject.github.io/guide/websockets.html#sending-messages

# @app.get("/{id}")
# async def get(id: int):
#     return HTMLResponse(html % id)

app.include_router(message.router, prefix="/chat-room/{room_id}")
app.include_router(chat_room.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)