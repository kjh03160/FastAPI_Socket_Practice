from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from pydantic import BaseModel


class LoginSchema(BaseModel):
    login_id: str
    password: str


class SignupSchema(LoginSchema):
    nickname: Optional[str] = ""
    password_2: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    exp: Any
    refresh_exp: Any
    login_id: str
    id: int


class UserSchema(BaseModel):
    username: str
    id: int
    login_id: str
    # password: str


class UserDisplaySchema(BaseModel):
    username: Optional[str]
    

class UserPrivacySchema(UserDisplaySchema):
    id: int
    login_id: str
    nickname: Optional[str] = None
    
    class Config:
        orm_mode = True


class UserToken(BaseModel):
    access_token: str
    refresh_token: str
