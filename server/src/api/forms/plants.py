from fastapi import Depends
from fastapi.params import Form

from src.api.forms.generic import ModelCreateForm
from src.api.forms.validators.plants import (
    ConditionsValidator,
    CreatorValidator,
    NameLengthValidator,
)
from src.api.middleware.context import context_middleware
from src.database.models import Plant


class PlantCreateForm(ModelCreateForm):
    """Form for creating plants.

    Additionally, stores the context.
    """

    model = Plant
    context: dict

    def __init__(
        self,
        context: dict = Depends(context_middleware),
        name: str = Form(...),
        description: str = Form(...),
        temperature: str = Form(...),
        humidity: str = Form(...),
    ):
        """Builds the data based on form dependencies."""
        super().__init__()
        self.data = {
            "name": name,
            "description": description,
            "temperature": temperature,
            "humidity": humidity,
            "creator": context.get("user"),
            "is_accepted": False,
        }
        self.validators = [NameLengthValidator, CreatorValidator, ConditionsValidator]
        self.context = context
