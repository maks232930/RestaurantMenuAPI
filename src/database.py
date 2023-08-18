from typing import AsyncGenerator

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import (
    DeclarativeMeta,
    Session,
    declarative_base,
    scoped_session,
    sessionmaker,
)

from src.config import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    REDIS_HOST,
    REDIS_PORT,
)

DATABASE_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
REDIS_URL: str = f'redis://{REDIS_HOST}:{REDIS_PORT}'

Base: DeclarativeMeta = declarative_base()

engine: AsyncEngine = create_async_engine(DATABASE_URL)
async_session_maker: sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

DATABASE_URL_SYNC = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine_sync: Engine = create_engine(DATABASE_URL_SYNC, echo=True)
SessionSync: scoped_session[Session] = scoped_session(sessionmaker(bind=engine_sync))


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
