"""Module to initialize the database."""

from app.db.base import Base
from app.db.session import async_engine


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
