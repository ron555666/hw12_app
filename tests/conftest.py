import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.database import get_session
from app.database_async import get_async_session
from app.dependency import get_current_user, get_current_user_async
from app import models
from app.models import User

TEST_DATABASE_URL = "sqlite:///./test.db"
TEST_ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# sync engine for normal routes
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# async engine for async routes
async_engine = create_async_engine(
    TEST_ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

AsyncTestingSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


def override_get_session():
    with Session(engine) as session:
        yield session


async def override_get_async_session():
    async with AsyncTestingSessionLocal() as session:
        yield session


def override_get_current_user():
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        hash_password="fakehashed"
    )


async def override_get_current_user_async():
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        hash_password="fakehashed"
    )


@pytest.fixture(scope="function")
def client():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_current_user_async] = override_get_current_user_async

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def unauthorized_client():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_async_session] = override_get_async_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)

