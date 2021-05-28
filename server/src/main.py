from fastapi import FastAPI

from .settings import settings


def create_application() -> FastAPI:
    """Initializes the FastAPI application."""
    application = FastAPI(
        title="Check My Plants",
        version=settings.VERSION,
        description="Simple REST Api made using FastAPI.",
    )
    return application


app = create_application()
