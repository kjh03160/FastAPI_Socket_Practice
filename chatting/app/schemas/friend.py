from pydantic import BaseModel
from typing import List, Optional

from .base import PaginationSchema


class FriendDetail(BaseModel):
    id: int
    nickname: Optional[str] = None


class FriendList(PaginationSchema):
    results: Optional[List[FriendDetail]] = []


class FriendCreateSchema(BaseModel):
    friend_login_id: str