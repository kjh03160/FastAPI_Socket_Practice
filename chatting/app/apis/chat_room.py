from fastapi import Depends, Path, Request, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from sqlalchemy.orm import Session

from typing import AsyncIterable

from app.database import app, get_db_sess, open_database_connection_pools, close_database_connection_pools
from app import schemas
from app import crud
from app.utils.auth import check_expired, get_user_id

router = InferringRouter()


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
