from typing import Optional

from fastapi import Depends, UploadFile
from fastapi.params import File, Form

from src.api.forms.generic import ModelCreateForm, ModelUpdateForm
from src.api.forms.validators.plants import ConditionsValidator, NameLengthValidator
from src.api.middleware.context import context_middleware
from src.database.models import Plant
from src.services.images import ImageService


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
        image: UploadFile = File(...),
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
            "image": image,
            "is_accepted": False,
        }
        self.validators = [NameLengthValidator, ConditionsValidator]
        self.context = context

    async def clean(self) -> None:
        """Adds an image object to the payload."""
        image = await ImageService.create_image(self.data["image"], "plant_images")
        self.data["image"] = image


class PlantEditForm(ModelUpdateForm):
    """Form for editing plants.

    Additionally, stores the context.
    """

    def __init__(
        self,
        context: dict = Depends(context_middleware),
        name: str = Form(...),
        description: str = Form(...),
        image: Optional[UploadFile] = File(...),
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
            "image": image,
            "creator": context.get("user"),
        }
        self.validators = [NameLengthValidator, ConditionsValidator]
        self.context = context

    async def clean(self) -> None:
        """Sets the image object if it was present in the payload."""
        image_file = self.data.pop("image")
        name_and_extension = image_file.filename.split(".")
        if len(name_and_extension) < 2 or not all(name_and_extension):
            return
        image = await ImageService.create_image(image_file, "plant_images")
        self.data["image"] = image
