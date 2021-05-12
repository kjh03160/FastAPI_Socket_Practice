from fastapi import Depends, Path, Request, status, Query, Body
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter, APIRouter

from sqlalchemy.orm import Session, joinedload

from typing import AsyncIterable

from app.database import get_db_sess, open_database_connection_pools, close_database_connection_pools
from app.utils.auth import check_expired, get_user_id, get_current_user
from app import schemas, crud, schemas, models

import logging
logger = logging.getLogger()

router = InferringRouter(
    tags=["friends"],
    responses={404: {"description": "Not found"}},
)

@cbv(router)
class Friend:
    request: Request
    user_id: int = Depends(get_user_id)
    db: Session = Depends(get_db_sess)
    
    @router.get("/", response_model=schemas.FriendList)
    async def get_friends(self):
        return crud.get_friends(self.db, self.user_id)
    
    @router.get('/{friend_id}', response_model=schemas.FriendDetail)
    async def get_friend_detail(self, friend_id: int = Query(...)):
        return crud.get_friend_detail(self.db, self.user_id, friend_id)
    
    @router.post("/")
    async def add_friend(self, data: schemas.FriendCreateSchema = Body(...)):
        return await crud.add_friend(self.db, self.user_id, data.friend_login_id)
    
    @router.delete("/{friend_id}")
    async def delete_friend(self):
        pass