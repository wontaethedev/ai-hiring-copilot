import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

user = os.getenv("POSTGRES_USER", "user")
password = os.getenv("POSTGRES_PASSWORD", "password")
host = os.getenv("POSTGRES_HOST", "db")
port = os.getenv("POSTGRES_PORT", 5432)
db = os.getenv("POSTGRES_DB", "platform")

def get_db_url(is_async=False):
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}" if is_async else f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_async_engine(get_db_url(is_async=True))

AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False, 
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
