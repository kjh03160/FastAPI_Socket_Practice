from .authentication import BasicAuthBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware import Middleware
from app.database import app
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])