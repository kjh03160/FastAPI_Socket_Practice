from fastapi.encoders import jsonable_encoder
from fastapi import BackgroundTasks, status, Request, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.param_functions import Query

from sqlalchemy import case, or_
from sqlalchemy.orm import Session, joinedload
from typing import Dict

from app import models, schemas
from app.utils import auth, pagination


async def get_friends(db: Session, user_id: int) -> schemas.FriendList:
    user = db.query(models.User).options(joinedload('friends')).get(user_id)
    friends = user.friends
    results = [schemas.FriendDetail(**jsonable_encoder(f)) for f in friends]
    
    output = schemas.FriendList(count=len(results), results=results)
    return output


async def get_friend_detail(db: Session, user_id: int, friend_id: int) -> schemas.FriendDetail:
    friend = db.query(models.User) \
            .join(models.FriendshipMapper, models.FriendshipMapper.user_id == models.User.id) \
            .filter(models.User.id == friend_id) \
            .first()
    
    if not friend:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return schemas.FriendDetail(**jsonable_encoder(friend))


async def add_friend(db: Session, user_id: int, friend_login_id: str) -> None: 
    user = db.query(models.User).options(joinedload('friends')) \
            .filter(or_(models.User.id == user_id, 
                        models.User.login_id == friend_login_id)) \
            .all()
    
    if len(user) < 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if user[0].add_friend(user[1]):
        db.add(user[0])
        db.commit()
        
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exists")


async def delete_friend(db: Session, user_id: int, friend_id: int) -> None:
    user = db.query(models.User).options(joinedload('friends')) \
                .filter(models.User.id.in_([user_id, friend_id])).all()
    
    if len(user) < 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if user[0].delete_friend(user[1]):
        db.add(user[0])
        db.commit()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
