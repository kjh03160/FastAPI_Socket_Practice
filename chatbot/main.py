from fastapi import Depends, Path, Query, Request, status, Response, WebSocket, \
                    BackgroundTasks, Body, Header
from fastapi.responses import HTMLResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from sqlalchemy.orm import Session

from typing import List, Dict, AsyncIterable, Optional

from app.database import app, get_db_sess, open_database_connection_pools, close_database_connection_pools
from app.connetion_manager import manager
from app import schemas
from app import crud
from app.utils.auth import check_expired, get_user_id

from redis import Redis
import uvicorn, json
import logging

router = InferringRouter()

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


@app.post("/signup", response_model=schemas.UserSchema)
async def signup(request: Request, data: schemas.SignupSchema, db: Session = Depends(get_db_sess)):
    user = await crud.create_user(db, data)
    return

@app.post("/login")
async def login(request: Request, data: schemas.LoginSchema, db: Session = Depends(get_db_sess)):
    user = await crud.login_user(db, data)
    return user


@app.get("/privacy")
async def get_privacy(request: Request, db: Session = Depends(get_db_sess)):
    return await crud.get_user_privacy(db, request)


@app.post("/refresh")
async def get_refresh_expired_token(request: Request, refresh_token: dict = Body(...), db: Session = Depends(get_db_sess)):
    return await crud.refresh(refresh_token['refresh_token'])


@cbv(router)
class ChatRoom:
    db: AsyncIterable[Session] = Depends(get_db_sess)
    request: Request
    user_id: int = Depends(get_user_id)

    @router.get("/chat-rooms")
    async def get_rooms(self):
        return await crud.get_chatting_room_list(self.request, self.db, self.user_id)
    
    @router.get("/chat-room/{room_id}")
    async def get_room_detail(self, room_id: int = Path(...)):
        return await crud.get_chatting_room_detail(self.request, self.db, room_id, self.user_id)

    @router.post("/chat-rooms", status_code=status.HTTP_201_CREATED, response_model=schemas.ChatRoomListSchema)
    async def post_chat_room(self, request_data: schemas.CreateChatRoomSchema):
        return await crud.create_chatting_room(self.request, self.db, request_data, self.user_id)

    @router.patch("/chat-room/{room_id}")
    async def patch_chat_room(self, data: schemas.UpdateChatRoomSchema, room_id: int = Path(...)):
        return await crud.update_chatting_room(self.request, self.db, room_id, data)

    @router.delete("/chat-room/{room_id}")
    async def delete_chat_room(self, room_id: int = Path(...)):
        return await crud.delete_chatting_room(self.request, self.db, room_id)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)