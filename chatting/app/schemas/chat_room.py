from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from .base import PaginationSchema
from pydantic import BaseModel


class CreateChatRoomSchema(BaseModel):
    users: List[int]
    name: str
    
    class Config:
        orm_mode = True


class DeleteChatRoomSchema(BaseModel):
    id: int
    
    class Config:
        orm_mode = True


class UpdateChatRoomSchema(BaseModel):
    roomd_id: int
    users: List[int]
    
    class Config:
        orm_mode = True
        
        
class ChatRoomAbstract(BaseModel):
    id: int
    name: str
    users: List
    create_user_id: int

    class Config:
        orm_mode = True


class ChatRoomListSchema(PaginationSchema):
    results: Optional[List[ChatRoomAbstract]] = []