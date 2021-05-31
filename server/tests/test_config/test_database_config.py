from unittest import mock
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient
from tortoise import Tortoise

from src.database.config import generate_schema
from src.main import app
from src.settings import settings


@mock.patch("src.database.config.register_tortoise")
def test_database_init(mock_register_tortoise: Mock):
    """Tests calling database functions."""
    with TestClient(app):
        mock_register_tortoise.assert_called_once()
        mock_register_tortoise.assert_called_with(
            app=app,
            db_url=settings.DATABASE_URL,
            modules={"models": settings.APP_MODELS},
            generate_schemas=False,
            add_exception_handlers=True,
        )


@pytest.mark.asyncio
@mock.patch.object(Tortoise, "close_connections")
@mock.patch.object(Tortoise, "generate_schemas")
@mock.patch.object(Tortoise, "init")
async def test_generate_schema(
    mock_init: Mock, mock_generate_schemas: Mock, mock_close_connections: Mock
):
    """Tests calling schema functions."""
    await generate_schema()
    mock_init.assert_called_once()
    mock_init.assert_called_with(
        db_url=settings.DATABASE_URL,
        modules={"models": settings.APP_MODELS},
    )
    mock_generate_schemas.assert_called_once()
    mock_close_connections.assert_called_once()
