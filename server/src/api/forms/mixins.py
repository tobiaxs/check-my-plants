from typing import Dict, Any

from src.database.models.generic import GenericModel


class FormCreateMixin:
    """Mixin with model creation implementation."""

    model: GenericModel
    data: Dict[str, Any]

    def clean(self) -> None:
        """Optional method for editing data before running create."""
        pass

    async def create(self) -> GenericModel:
        """Creates and returns a model instance based on the data."""
        self.clean()
        instance = await self.model.create(**self.data)
        return instance
