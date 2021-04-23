from fastapi import Depends, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from typing import Optional, Dict
from calendar import timegm

from app.settings import JWT_SETTING
from app.models import User
from app.schemas import Token, UserSchema, UserDisplaySchema, UserToken, UserPrivacySchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, login_id: str):
    user = db.query(User).filter_by(login_id=login_id).first()
    if user:
        user_dict = jsonable_encoder(user)
    return UserSchema(**user_dict)


def create_token(data: UserDisplaySchema) -> Dict[str, UserToken]:
    access_to_encode = data.dict() if not isinstance(data, dict) else data
    refresh_to_encode = access_to_encode.copy()
    expire = datetime.utcnow() + JWT_SETTING['ACCESS_TOKEN_EXPIRE']
    access_to_encode.update({"exp": expire})

    refresh_expire = timegm((datetime.utcnow() + JWT_SETTING['REFRESH_TOKEN_EXPIRE']).utctimetuple()) 
    refresh_to_encode.update({'refresh_exp': refresh_expire})

    access_token = Token(**access_to_encode)
    refresh_token = Token(**refresh_to_encode)

    access_jwt = jwt.encode(access_token.dict(), JWT_SETTING['SECRET_KEY'], algorithm=JWT_SETTING['ALGORITHM'])
    refresh_jwt = jwt.encode(refresh_token.dict(), JWT_SETTING['SECRET_KEY'], algorithm=JWT_SETTING['ALGORITHM'])

    return access_jwt, refresh_jwt


def authenticate_user(db: Session, login_id: str, password: str):
    user = get_user(db, login_id)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    user = jsonable_encoder(user)
    access_jwt, refresh_jwt = create_token(UserSchema(**user))
    data = UserToken(access_token=access_jwt, refresh_token=refresh_jwt).dict()
    data.update({'username': user['username']})
    return data


async def get_current_user(db: Session = None, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        check_expired(payload['exp'])
        login_id: str = payload.get("login_id")
        if login_id is None:
            raise credentials_exception
    except JWTError as e:  
        print(e)
        raise credentials_exception
    if db:
        user = get_user(db, login_id=login_id)
        if user is None:
            raise credentials_exception
    return UserPrivacySchema(**jsonable_encoder(user))


async def get_user_id(authorization: str = Header(...)) -> int:
    if authorization:
        payload = decode_jwt(authorization)
        check_expired(payload['exp'])
        return payload['id']


async def get_user_obj_by_id(db: Session, user_id: int) -> object:
    user = db.query(User).get(user_id)
    return user


def decode_jwt(token: str = Depends(oauth2_scheme)):
    token = token.split()[1]
    payload = jwt.decode(token, JWT_SETTING['SECRET_KEY'], algorithms=[JWT_SETTING['ALGORITHM']], options={"verify_exp": False})
    return payload


def check_expired(token: str):
    expire_time = datetime.fromtimestamp(token)
    if expire_time < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")


async def refresh_expired_access_token(refresh_token: str):
    refresh_jwt = decode_jwt(refresh_token)
    check_expired(refresh_jwt['refresh_exp'])
    access_jwt, refresh_jwt = create_token(refresh_jwt)
    return UserToken(access_token=access_jwt, refresh_token=refresh_jwt)