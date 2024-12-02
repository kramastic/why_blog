from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


DATABASE_PARAMS = {}

engine = create_async_engine(settings.DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
        )
