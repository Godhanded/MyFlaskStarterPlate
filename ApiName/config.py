import os
import datetime
from dotenv import load_dotenv


load_dotenv(".env")


class App_Config:
    SESSION_TYPE = "filesystem" if not os.getenv("PROD", None) else "sqlalchemy"
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_HTTPONLY = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///test.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("USER_NAME")
    MAIL_PASSWORD = os.environ.get("PASS")

    CACHE_TYPE = "FileSystemCache"
    CACHE_DIR = "cache"
