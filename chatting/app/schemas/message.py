from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from datetime import date as DATE
from pydantic import BaseModel

from .base import PaginationSchema
from .user import UserPrivacySchema


class MessageSchema(BaseModel):
    id: int
    user_id: int
    nickname: Optional[str] = None
    content: str
    create_dt: DATE
    read_dt: DATE


class MessageListSchema(PaginationSchema):
    results: Optional[List[MessageSchema]] = []