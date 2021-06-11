from abc import ABC, abstractmethod
from typing import Any, Dict

from src.api.forms.mixins import FormCreateMixin


class GenericForm(ABC):
    """Generic form class with init logic and abstract validate method."""

    def __init__(self, *args, **kwargs):
        """Initializes errors as an empty list.
        Inheritors should assign the form values to data.
        """
        self.errors = []
        self.data: Dict[str, Any]

    @abstractmethod
    def validate(self) -> None:
        """Validates given data and saves the errors."""
        raise NotImplementedError()


class ModelCreateForm(GenericForm, FormCreateMixin, ABC):
    """Abstract create form class."""
