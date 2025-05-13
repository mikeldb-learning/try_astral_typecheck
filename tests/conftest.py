import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.main import app
from app.plants.infrastructure import PostgresPlantRepository, PostgresPlantsUoW


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@database:5432/postgres_test",
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Create a test database session."""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def test_client(test_session):
    """Create a test client with the test database session."""

    async def override_get_db():
        yield test_session

    app.dependency_overrides[PostgresPlantRepository] = (
        lambda: PostgresPlantRepository()
    )
    app.dependency_overrides[PostgresPlantsUoW] = lambda: PostgresPlantsUoW(
        plant_repository=PostgresPlantRepository()
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
