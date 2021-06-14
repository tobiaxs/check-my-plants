from typing import Any, Dict

from src.database.models.generic import GenericModel


class FormCreateMixin:
    """Mixin with model creation implementation."""

    model: GenericModel
    data: Dict[str, Any]

    def clean(self) -> None:
        """Optional method for editing data before running create."""

    async def create(self) -> "model":
        """Creates and returns a model instance based on the data."""
        self.clean()
        instance = await self.model.create(**self.data)
        return instance
