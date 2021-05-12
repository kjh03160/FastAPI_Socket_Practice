from datetime import datetime, timedelta
import os

DEFAULT_DATABASES = {
    "USER": os.getenv('DB_USER'),
    "PASSWORD": os.getenv('DB_PASSWORD'),
    "HOST": os.getenv('DB_HOST'),
    "PORT": os.getenv('DB_PORT'),
    "NAME": os.getenv('DB_NAME')
}

REDIS_URL = os.getenv('REDIS_URL')

JWT_SETTING = {
    "SECRET_KEY": "73cb0d7d6240187d6d33df85480daf3994b011828e8db3c18a970c7095cee578",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE": timedelta(minutes=60),
    "REFRESH_TOKEN_EXPIRE": timedelta(minutes=1 * 24 * 60 * 60)
}
DATABASE_URL = f"postgresql://{DEFAULT_DATABASES['USER']}:" \
               f"{DEFAULT_DATABASES['PASSWORD']}" \
               f"@{DEFAULT_DATABASES['HOST']}" \
               f":{DEFAULT_DATABASES['PORT']}" \
               f"/{DEFAULT_DATABASES['NAME']}"
               
