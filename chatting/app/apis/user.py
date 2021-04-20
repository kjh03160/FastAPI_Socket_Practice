from fastapi import Depends, Request, Body
from sqlalchemy.orm import Session

from app.database import app, get_db_sess
from app import crud, schemas


@app.post("/signup", response_model=schemas.UserSchema)
async def signup(request: Request, data: schemas.SignupSchema, db: Session = Depends(get_db_sess)):
    user = await crud.create_user(db, data)
    return user

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