import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Class containing application settings."""

    TITLE: str = "Check My Plants"
    VERSION: str = os.getenv("VERSION")
    DESCRIPTION: str = (
        "Simple application for cataloging and viewing home plants made using FastAPI."
    )

    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SUPERUSER_EMAIL: str = os.getenv("SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD")

    APP_MODELS: list[str] = [
        "src.database.models",
        # TODO: Add aerich migrations
        # "aerich.models"
    ]


settings = Settings()
