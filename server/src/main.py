import logging

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.api.v1.users import router as users_router
from src.database.base_class import Base
from src.database.session import engine
from src.settings import settings

logger = logging.getLogger(__name__)


def include_routers(application: FastAPI):
    """Adds the routers."""
    application.include_router(users_router, prefix="/users", tags=["users"])


def configure_static(application: FastAPI):
    """Prepares a folder with the static files."""
    application.mount("/static", StaticFiles(directory="static"), name="static")


async def create_tables():
    """Prepares the SQLAlchemy engine."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_application() -> FastAPI:
    """Initializes the FastAPI application."""
    application = FastAPI(
        title="Check My Plants",
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )
    configure_static(application)
    include_routers(application)
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    await create_tables()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
