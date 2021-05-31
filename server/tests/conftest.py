from collections import Generator

import nest_asyncio
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from tortoise.contrib.test import finalizer, initializer

from src.main import create_application
from src.settings import settings


@pytest.fixture
async def client() -> Generator[AsyncClient]:
    """Async client with test database connection."""
    nest_asyncio.apply()
    initializer(modules=settings.APP_MODELS)
    app = create_application()
    async with AsyncClient(
        app=app, base_url="https://testserver"
    ) as test_client, LifespanManager(app):
        yield test_client
    finalizer()
