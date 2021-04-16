from fastapi import Depends, Path, Query, Request, status, Response, WebSocket, \
                    BackgroundTasks, Body
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from typing import List, Dict

from app.database import app, get_db_sess, open_database_connection_pools, close_database_connection_pools
from app.connetion_manager import manager
from app.schemas import SignupSchema, UserSchema, LoginSchema
from app.crud import create_user, login_user, get_user_privacy, refresh
from app.utils.auth import check_expired

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

html = ""
with open('index.html', 'r') as f:
    html = f.read()



# https://bocadilloproject.github.io/guide/websockets.html#sending-messages

# @app.get("/{id}")
# async def get(id: int):
#     return HTMLResponse(html % id)


@app.post("/signup", response_model=UserSchema)
async def signup(request: Request, data: SignupSchema, db: Session = Depends(get_db_sess)):
    user = await create_user(db, data)
    return

@app.post("/login")
async def login(request: Request, data: LoginSchema, db: Session = Depends(get_db_sess)):
    user = await login_user(db, data)
    return user


@app.get("/privacy")
async def get_privacy(request: Request, db: Session = Depends(get_db_sess)):
    return await get_user_privacy(db, request)


@app.get("/refresh")
async def get_refresh_expired_token(request: Request, db: Session = Depends(get_db_sess)):
    return await refresh(request)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)