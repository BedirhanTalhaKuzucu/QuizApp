from .base import *

# DEBUG = False
DEBUG = False  # Lokalde denenmek istendiğinde True yapılmalı

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("SQL_DATABASE"),
        "USER": config("SQL_USER"),
        "PASSWORD": config("SQL_PASSWORD"),
        "HOST": config("SQL_HOST"),
        "PORT": config("SQL_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}

DISABLE_COLLECTSTATIC = 1
