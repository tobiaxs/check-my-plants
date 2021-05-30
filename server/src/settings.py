import os


class Settings:
    """Class containing application settings."""

    VERSION: str = os.getenv("VERSION")
    DESCRIPTION: str = (
        "Simple application for cataloging and viewing home plants made using FastAPI."
    )
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()
