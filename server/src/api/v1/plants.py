from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.middleware.authentication import user_middleware
from src.database.crud.plants import (
    create_plant,
    delete_plant,
    get_all_plants,
    get_plant,
)
from src.database.models import User
from src.schemas.plants import PlantCreate, PlantModel, PlantQuerySet

router = APIRouter()


@router.post("/", status_code=201, response_model=PlantModel)
async def plant_create(
    payload: PlantCreate, user: User = Depends(user_middleware)
) -> PlantModel:
    """Creates a new plant instance."""
    plant = await create_plant(payload, user)
    return plant


@router.get("/", status_code=200, response_model=PlantQuerySet)
async def plants_list() -> PlantQuerySet:
    """Retrieves a list of all accepted plants."""
    plants = await get_all_plants()
    return plants


@router.get("/{pk}/", status_code=200, response_model=PlantModel)
async def plant_retrieve(pk: UUID) -> PlantModel:
    """Retrieves a specific plant by it's pk."""
    plant = await get_plant(pk)
    return plant


@router.delete("/{pk}/", status_code=200, response_model=bool)
async def plant_delete(pk: UUID, user: User = Depends(user_middleware)) -> bool:
    """Deletes a specific plant by it's pk."""
    deleted = await delete_plant(pk, user)
    return deleted
