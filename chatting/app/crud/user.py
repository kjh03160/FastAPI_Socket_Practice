from fastapi.encoders import jsonable_encoder
from fastapi import BackgroundTasks, status
from fastapi.responses import JSONResponse, Response
from fastapi.param_functions import Query

from sqlalchemy import case
from sqlalchemy.orm import Session
from fastapi import Request
from typing import Dict

from app import models, schemas
from app.utils.auth import get_password_hash, authenticate_user, get_current_user, refresh_expired_access_token, \
                            destroy_token

async def create_user(db: Session, data: schemas.SignupSchema):
    if data.password == data.password_2:
        hashed_pw = get_password_hash(data.password)
        user = models.User(login_id=data.login_id, password=hashed_pw, nickname=data.nickname)
        db.add(user)
        db.commit()
        db.refresh(user)
        return jsonable_encoder(user)


async def login_user(db: Session, data: schemas.LoginSchema):
    user = authenticate_user(db, **data.dict())
    if user:
        return user


async def get_user_privacy(db: Session, request: Request):
    token = request.headers.get('authorization', None)
    if token:
        return await get_current_user(request, db, token)
    return Response("Token doesn't exist", status_code=status.HTTP_401_UNAUTHORIZED)


async def refresh(refresh_token: str):
    return await refresh_expired_access_token(refresh_token)

async def logout(request: Request, authorization: str) -> None:
    destroy_token(authorization)