from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

import base64
import binascii

from app.utils.auth import decode_jwt, check_expired, get_user_obj_by_id
from app.database import get_db_sess, get_db_conn

class BasicAuthBackend(AuthenticationBackend):
    
    async def authenticate(self, request: Request):
        if "Authorization" not in request.headers:
            return

        header = request.headers["Authorization"]
        try:
            if not header.lower().startswith('bearer'):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            decoded = decode_jwt(header)
            check_expired(decoded['exp'])
        except (ValueError, UnicodeDecodeError, HTTPException) as exc:
            raise AuthenticationError('Invalid basic auth credentials')
        db = Session(bind= await get_db_conn())
        user = await get_user_obj_by_id(db, decoded['id'])
        db.close()
        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), user


