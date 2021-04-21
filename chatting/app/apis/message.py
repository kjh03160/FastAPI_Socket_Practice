from fastapi import Depends, Path, Request, status, Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter, APIRouter

from sqlalchemy.orm import Session

from typing import AsyncIterable

from app.database import get_db_sess, open_database_connection_pools, close_database_connection_pools
from app import schemas
from app import crud
from app.utils.auth import check_expired, get_user_id


router = InferringRouter(
    tags=["messages"],
    responses={404: {"description": "Not found"}},
)

@cbv(router)
class Message:
    db: AsyncIterable[Session] = Depends(get_db_sess)
    request: Request
    user_id: int = Depends(get_user_id)
    room_id: int = Path(...)
    
    @router.get("/messages")
    async def get_message_list(self, page: int = Query(1), page_size: int = Query(20)):
        return await crud.get_message_list(self.request, self.db, self.room_id, self.user_id, page, page_size)
    
    @router.post("/messages")
    async def create_message(self, data: schemas.MessageCreateSchema):
        return await crud.create_message(self.request, self.db, self.room_id, self.user_id, data)