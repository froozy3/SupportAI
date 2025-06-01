from database import get_async_session


async def get_session():
    async with get_async_session() as session:
        yield session
