from datetime import datetime, timedelta


DATABASE_URL = "postgresql://postgres:hwaitaeng1@localhost:5431/juna"


JWT_SETTING = {
    "SECRET_KEY": "73cb0d7d6240187d6d33df85480daf3994b011828e8db3c18a970c7095cee578",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE": timedelta(minutes=60),
    "REFRESH_TOKEN_EXPIRE": timedelta(minutes=1 * 24 * 60 * 60)
}
