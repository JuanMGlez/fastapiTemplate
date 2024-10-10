# app/db/postgres.py
# mypy: ignore-errors
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Base class for the database models
Base = declarative_base()


DATEBASE_URL = settings.DATABASE_URL

# Asynchronous engine and session
async_engine = create_async_engine(DATEBASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_async_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session