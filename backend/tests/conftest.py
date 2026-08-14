from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database import get_database_session
from app.main import app
from tests.database import test_engine


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with test_engine.connect() as connection:
        transaction = await connection.begin()

        test_session_factory = async_sessionmaker(
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        async def override_get_database_session() -> AsyncIterator[AsyncSession]:
            async with test_session_factory() as session:
                yield session

        app.dependency_overrides[get_database_session] = override_get_database_session

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            yield client

        app.dependency_overrides.clear()
        await transaction.rollback()

    await test_engine.dispose()
