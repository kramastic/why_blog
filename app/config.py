import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_NAME: str = os.environ.get("DB_NAME")

    SECRET_JWT_KEY: str = os.environ.get("SECRET_JWT_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")

    SMTP_PORT: int = os.environ.get("SMTP_PORT")
    SMTP_HOST: str = os.environ.get("SMTP_HOST")
    SMTP_USER: str = os.environ.get("SMTP_USER")
    SMTP_PASS: str = os.environ.get("SMTP_PASS")

    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_PORT: int = os.environ.get("REDIS_PORT")

    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


settings = Settings()
