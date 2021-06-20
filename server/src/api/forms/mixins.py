from abc import ABC
from typing import Any, Dict, Type

from src.database.models.generic import GenericModel


class GenericCrudMixin(ABC):
    """Mixin with properties that are needed in every crud operation."""

    model: Type[GenericModel]
    data: Dict[str, Any]

    async def clean(self) -> None:
        """Optional method for editing data before running crud method."""


class FormCreateMixin(GenericCrudMixin):
    """Mixin with model creation implementation."""

    async def create(self) -> GenericModel:
        """Creates and returns a model instance based on the data."""
        await self.clean()
        instance = await self.model.create(**self.data)
        return instance


class FormUpdateMixin(GenericCrudMixin):
    """Mixin with model creation implementation."""

    async def update(self, instance: GenericModel) -> GenericModel:
        """Update and returns a model instance based on the data."""
        await self.clean()
        instance = instance.update_from_dict(data=self.data)
        await instance.save()
        return instance
