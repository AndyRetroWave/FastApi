from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import setting

if setting.MODE == "TEST":
    DATEBASE_URL = f"postgresql+asyncpg://{setting.TEST_DB_USER}:{setting.TEST_DB_PASS}@{setting.TEST_DB_HOST}:{setting.TEST_DB_PORT}/{setting.TEST_DB_NAME}"
    DATABASE_PARAM = {"poolclass": NullPool}
else:
    DATEBASE_URL = f"postgresql+asyncpg://{setting.DB_USER}:{setting.DB_PASS}@{setting.DB_HOST}:{setting.DB_PORT}/{setting.DB_NAME}"
    DATABASE_PARAM = {}

engine = create_async_engine(DATEBASE_URL, **DATABASE_PARAM)

async_session_maker = sessionmaker(engine, 
                                   class_=AsyncSession, 
                                   expire_on_commit=False
                                   )

class Base(DeclarativeBase):
    pass