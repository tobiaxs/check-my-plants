from collections import Generator
from unittest.mock import mock_open, patch

import nest_asyncio
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pydantic import SecretStr
from tortoise.contrib.test import finalizer, initializer

from src.database.models import User
from src.main import create_application
from src.services.hashing import HashingService
from src.services.jwt_token import JwtTokenService
from src.settings import settings

TEST_USER_EMAIL = "pytest@auth.com"
TEST_USER_PASSWORD = HashingService.get_hashed_password(SecretStr("pytest-auth-user"))


@pytest.fixture(scope="session", autouse=True)
def create_file_mock() -> Generator[None]:
    """Mocks the create file function logic to prevent adding files in tests."""
    with patch("src.services.images.open", mock_open()):
        with patch("src.services.images.shutil.copyfileobj"):
            yield


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


@pytest.fixture
async def auth_client(client: AsyncClient) -> Generator[AsyncClient]:
    """Authenticated async client."""
    user = await User.create(email=TEST_USER_EMAIL, hashed_password=TEST_USER_PASSWORD)
    token = JwtTokenService.encode_jwt(user.email)
    client.headers["Authorization"] = f"Bearer {token.access_token}"
    yield client


@pytest.fixture
async def cookie_client(client: AsyncClient) -> Generator[AsyncClient]:
    """Async client with cookie."""
    user = await User.create(email=TEST_USER_EMAIL, hashed_password=TEST_USER_PASSWORD)
    token = JwtTokenService.encode_jwt(user.email)
    client.cookies = {"access_token": f"Bearer {token.access_token}"}
    yield client
