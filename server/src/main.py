import logging

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.api.v1.jinja.plants import router as plants_jinja_router
from src.api.v1.plants import router as plants_api_router
from src.api.v1.users import router as users_api_router
from src.database.config import init_database
from src.settings import settings

logger = logging.getLogger(__name__)


def include_routers(application: FastAPI):
    """Adds the api and jinja routers."""
    application.include_router(users_api_router)
    application.include_router(plants_api_router)
    application.include_router(plants_jinja_router)


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
    include_routers(application)
    configure_static(application)
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    init_database(app)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
