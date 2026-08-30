import asyncio
from sqlalchemy import text

from app.database.connection import engine, async_session_factory


async def main() -> None:
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        print(result.scalar_one(), "engine ok")

    async with async_session_factory() as session:
        result = await session.execute(text("SELECT 1"))
        print(result.scalar_one(), "factory ok")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())