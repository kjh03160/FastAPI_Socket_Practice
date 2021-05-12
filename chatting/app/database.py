from typing import AsyncIterable, Optional

from fastapi import Depends, FastAPI
from fastapi_utils.api_settings import get_api_settings

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine as Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.settings import DATABASE_URL

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def get_app() -> FastAPI:
    get_api_settings.cache_clear()
    settings = get_api_settings()
    settings.debug = True
    app = FastAPI(**settings.fastapi_kwargs)
    return app

application = app = get_app()

_db_conn: Optional[Database]


async def open_database_connection_pools():
    global _db_conn
    _db_conn = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=_db_conn)
    return


async def close_database_connection_pools():
    global _db_conn
    if _db_conn:
        _db_conn.dispose()


async def get_db_conn() -> Database:
    assert _db_conn is not None
    return _db_conn


async def get_db_sess(db_conn=Depends(get_db_conn)) -> AsyncIterable[Session]:
    sess = Session(bind=db_conn)
    try:
        yield sess
    finally:
        sess.close()


Base = declarative_base()
