from uuid import UUID

from fastapi import HTTPException, UploadFile

from src.database.models import Plant, User
from src.schemas.plants import PlantCreate, PlantModel, PlantQuerySet
from src.services.images import ImageService


async def create_plant(
    payload: PlantCreate, image_file: UploadFile, user: User
) -> PlantModel:
    """Creates a new plant instance."""
    image = await ImageService.create_image(image_file, "plant_images")
    plant = await Plant.create(
        **payload.dict(), creator=user, image=image, is_accepted=False
    )
    plant_model = PlantModel.from_orm(plant)
    return plant_model


async def get_all_plants() -> PlantQuerySet:
    """Retrieves a list of all accepted plants."""
    plants = Plant.filter(is_accepted=True)
    plant_models = await PlantQuerySet.from_queryset(plants)
    return plant_models


async def get_plant(pk: UUID) -> PlantModel:
    """Retrieves a single plant by its pk."""
    plant = await get_plant_or_404(pk)
    plant_model = PlantModel.from_orm(plant)
    return plant_model


async def delete_plant(pk: UUID, user: User) -> bool:
    """Deletes a given plant if user is its owner or a superuser."""
    plant = await get_plant_or_404(pk)
    if plant.creator != user and not user.is_superuser:
        raise HTTPException(
            status_code=403, detail="You are not allowed to perform this action"
        )
    await plant.delete()
    return True


async def get_plant_or_404(pk: UUID):
    """Retrieves and returns a plant or raises an 404 if it does not exist."""
    plant = await Plant.get_or_none(pk=pk)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant does not exist")
    await plant.fetch_related("creator")
    return plant
