from fastapi import FastAPI
from pydantic import SecretStr
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from src.database.models import User
from src.services.hashing import HashingService
from src.settings import settings

"""Tortoise settings."""
TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": settings.APP_MODELS,
            "default_connection": "default",
        }
    },
}


def init_database(app: FastAPI) -> None:
    """Initializes database connection with Tortoise."""
    register_tortoise(
        app=app,
        db_url=settings.DATABASE_URL,
        modules={"models": settings.APP_MODELS},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def create_superuser() -> None:
    """Creates a starting superuser."""
    await User.get_or_create(
        email=settings.SUPERUSER_EMAIL,
        hashed_password=HashingService.get_hashed_password(
            SecretStr(settings.SUPERUSER_PASSWORD)
        ),
        is_superuser=True,
    )


async def generate_schema() -> None:
    """Generates database schemas with Tortoise."""
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": settings.APP_MODELS},
    )
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()
