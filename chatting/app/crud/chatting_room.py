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

async def get_chatting_room_list(request: Request, db: Session, user_id: int):
    user = await auth.get_user_obj_by_id(db, user_id)
    chatting_rooms = user.rooms
    
    results = []
    for room in chatting_rooms:
        room_info = jsonable_encoder(room)
        schema = schemas.ChatRoomAbstract(**room_info, users=[user.id for user in room.users])
        results.append(schema)
    
    return schemas.ChatRoomListSchema(results=results, count=len(results))


async def get_chatting_room_detail(request: Request, db: Session, room_id: int, user_id: int):
    room = db.query(models.ChattingRoom).get(room_id)
    if room:
        return schemas.ChatRoomAbstract(**jsonable_encoder(room), users=[user.nickname for user in room.users])
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def create_chatting_room(reqeust: Request, db: Session, data: schemas.CreateChatRoomSchema, user_id: int):
    chatroom = models.ChattingRoom(name=data.name, create_user_id=user_id)
    chatroom.users = db.query(models.User).filter(models.User.id.in_(data.users)).all()
    db.add(chatroom)
    db.commit()
    db.refresh(chatroom)
    return jsonable_encoder(chatroom)


async def delete_chatting_room(request: Request, db: Session, room_id: int):
    chatroom = db.query(models.ChattingRoom).get(room_id)
    db.delete(chatroom)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def update_chatting_room(request: Request, db: Session, data: schemas.UpdateChatRoomSchema, room_id: int):
    usrs = db.query(models.User).filter(models.User.id.in_(data.users)).all()
    room = db.query(models.ChatRoom).get(room_id)
    room.users = usrs
    
    flag_modified(room, 'users')
    db.add(room)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
