from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import Session

DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/hw12_app"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)


async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session