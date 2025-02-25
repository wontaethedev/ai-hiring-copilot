import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from contextlib import asynccontextmanager

from settings import postgres_settings

user = postgres_settings.USER
password = postgres_settings.PASSWORD
host = postgres_settings.HOST
port = postgres_settings.PORT
db = postgres_settings.DB

def get_db_url(is_async=False):
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}" if is_async else f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_async_engine(get_db_url(is_async=True))

AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False, 
)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@asynccontextmanager
async def get_context_managed_session():
    async with AsyncSessionLocal() as db:
        yield db
