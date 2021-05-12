from .authentication import BasicAuthBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from app.database import app
from fastapi.middleware.trustedhost import TrustedHostMiddleware

