from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_queryset_creator

from src.database.models import Plant
from src.database.models.enums import Conditions
from src.schemas.generic import BaseOrmModel, as_form
from src.schemas.users import UserModelUuid


@as_form
class PlantCreate(BaseModel):
    """Payload needed for plant creation."""

    name: str
    description: str
    temperature: Conditions = Conditions.average
    humidity: Conditions = Conditions.average


class PlantModel(BaseOrmModel, PlantCreate):
    """Payload containing whole plant instance with creators uuid."""

    is_accepted: bool
    creator: UserModelUuid


"""List of plant payloads."""
PlantQuerySet = pydantic_queryset_creator(Plant, exclude=("description", "is_accepted"))
