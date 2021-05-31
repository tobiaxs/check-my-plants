from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

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


async def generate_schema() -> None:
    """Generates database schemas with Tortoise."""
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": settings.APP_MODELS},
    )
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()
