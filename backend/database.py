import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from constans import DATABASE_URL
from models import BaseDB

engine = create_async_engine(DATABASE_URL)


async_session_maker = sessionmaker(engine, class_=AsyncSession)


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseDB.metadata.drop_all)
        await conn.run_sync(BaseDB.metadata.create_all)


async def main():
    await create_all_tables()


if __name__ == "__main__":
    asyncio.run(main())
