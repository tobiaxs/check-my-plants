import logging

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.api.v1.users import router as users_router
from src.database.config import init_database
from src.settings import settings

logger = logging.getLogger(__name__)


def include_routers(application: FastAPI):
    """Adds the routers."""
    application.include_router(users_router, prefix="/users", tags=["users"])


def configure_static(application: FastAPI):
    """Prepares a folder with the static files."""
    application.mount("/static", StaticFiles(directory="static"), name="static")


def create_application() -> FastAPI:
    """Initializes the FastAPI application."""
    application = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    include_routers(app)
    init_database(app)
    configure_static(app)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
