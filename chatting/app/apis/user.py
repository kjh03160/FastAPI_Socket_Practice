from fastapi import Depends, Request, Body, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import app, get_db_sess
from app import crud, schemas


@app.post("/signup", response_model=schemas.UserPrivacySchema)
async def signup(data: schemas.SignupSchema, db: Session = Depends(get_db_sess)):
    try:
        user = await crud.create_user(db, data)
        if not user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Password doesn't match")
        return user
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Already exist")


@app.post("/login")
async def login(request: Request, data: schemas.LoginSchema, db: Session = Depends(get_db_sess)):
    user = await crud.login_user(db, data)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credential Denied")
    
    res = JSONResponse(user, headers={'Authorization': "Bearer " + user['access_token']})
    return res


@app.get("/privacy")
async def get_privacy(request: Request, db: Session = Depends(get_db_sess)):
    return await crud.get_user_privacy(db, request)


@app.post("/refresh")
async def get_refresh_expired_token(request: Request, refresh_token: dict = Body(...), db: Session = Depends(get_db_sess)):
    return await crud.refresh(refresh_token['refresh_token'])


@app.post("/logout")
async def logout(request: Request):
    token = request.headers.get('authorization')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    await crud.destroy_token(token)
    
    return JSONResponse(status_code=status.HTTP_200_OK)