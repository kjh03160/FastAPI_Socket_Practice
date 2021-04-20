from datetime import date as DATE

from pydantic import BaseModel


class AbstractBase(BaseModel):
    created_dt: DATE
    updated_dt: DATE


class PaginationSchema(BaseModel):
    count: int
    next: str = None
    prev: str = None
