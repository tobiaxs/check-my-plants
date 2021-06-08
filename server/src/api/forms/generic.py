from abc import ABC, abstractmethod
from typing import Any, Dict

from src.api.forms.mixins import FormCreateMixin


class GenericForm(ABC):
    """Generic form class with init logic and abstract validate method."""

    def __init__(self, data: Dict[str, Any]):
        """Initializes errors as empty list and saves the data."""
        self.errors = []
        self.data = data

    @abstractmethod
    def validate(self) -> None:
        """Validates given data and saves the errors."""
        raise NotImplementedError()


class ModelCreateForm(GenericForm, FormCreateMixin, ABC):
    """Abstract create form class."""
