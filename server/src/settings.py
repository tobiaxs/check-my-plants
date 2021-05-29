import os


class Settings:
    """Class containing application settings."""

    VERSION: str = os.getenv("VERSION")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()
