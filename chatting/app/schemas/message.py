from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from datetime import date as DATE
from pydantic import BaseModel

from app.settings import TIMEZONE
from .base import PaginationSchema
from .user import UserPrivacySchema


class MessageCreateSchema(BaseModel):
    room_id: int
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None
    content: str
    create_dt: Optional[DATE] = datetime.now(TIMEZONE)
    read_dt: Optional[DATE] = datetime.now(TIMEZONE)

    class Config:
        orm_mode = True
    
class MessageSchema(BaseModel):
    id: int
    user_id: int
    nickname: Optional[str] = None
    content: str
    create_dt: Optional[DATE]
    read_dt: Optional[DATE]


class MessageListSchema(PaginationSchema):
    results: Optional[List[MessageSchema]] = []