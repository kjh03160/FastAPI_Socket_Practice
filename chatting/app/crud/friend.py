from fastapi.encoders import jsonable_encoder
from fastapi import BackgroundTasks, status, Request, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.param_functions import Query

from sqlalchemy import case
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import Dict

from app import models, schemas
from app.utils import auth, pagination


async def get_friends(db: Session, user_id: int) -> schemas.FriendList:
    user = self.db.query(models.User).options(joinedload('friends')).get(self.user_id)
    friends = user.friends
    results = [schemas.FriendDetail(**jsonable_encoder(f)) for f in friends]
    
    output = schemas.FriendList(count=len(results), results=results)
    return output


async def get_friend_detail(db: Session, user_id: int, friend_id: int) -> schemas.FriendDetail:
    user = self.db.query(models.User).options(joinedload('friends')).get(self.user_id)
    friendship = self.db.query(models.User, models.friendship) \
                        .filter(models.friendship.user_id == friend_id,
                                models.friendship.friend_id == self.request.user.id)

    friend = self.db.query(models.User).get(friend_id)
    return schemas.FriendDetail(**jsonable_encoder(friend))


async def add_friend(db: Session, user_id: int, friend_login_id: str):
    users = self.db.query(models.User).filter(models.User.id.in_([user_id, friend_id])).all()
    if len(users) < 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    user1 = user[0]
    user1.add_friend(users[1])
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)