# main.py
import os
from typing import AsyncGenerator, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from index import main_wrap

load_dotenv()


def get_async_engine():
    database_url = os.getenv('DATABASE_URL')
    if database_url is None:
        raise ValueError('DATABASE_URL environment variable is not set')

    return create_async_engine(database_url)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    engine = get_async_engine()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def main():
    async for session in get_async_session():
        async with session.begin():
            await main_wrap(session, '서울특별시', '약국', 'PM9')
        await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
