from abc import ABC
from asyncio import iscoroutinefunction
from typing import Any, Dict, Type

from src.api.forms.mixins import FormCreateMixin, FormUpdateMixin
from src.api.forms.validators.generic import GenericValidator


class GenericForm(ABC):
    """Generic form class with init logic and abstract validate method."""

    def __init__(self, *args, **kwargs):
        """Initializes errors as an empty list.
        Inheritors should assign the form values to data.
        """
        self.errors: list[str] = []
        self.data: Dict[str, Any] = {}
        self.validators: list[Type[GenericValidator]] = []

    async def validate(self) -> None:
        """Runs the validators and merge the errors lists.

        If validator is async, awaits the coroutine.
        """
        for validator_class in self.validators:
            validator = validator_class()
            if iscoroutinefunction(validator.validate):
                await validator.validate(self.data)
            else:
                validator.validate(self.data)
            self.errors += validator.errors


class ModelCreateForm(GenericForm, FormCreateMixin, ABC):
    """Abstract create form class."""


class ModelUpdateForm(GenericForm, FormUpdateMixin, ABC):
    """Abstract update form class."""
