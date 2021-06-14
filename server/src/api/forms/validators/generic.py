from abc import ABC, abstractmethod


class GenericValidator(ABC):
    """Interface for form validators."""

    def __init__(self):
        """Errors are initialized are an empty list."""
        self.errors: list[str] = []

    @abstractmethod
    def validate(self, data: dict):
        """Method for checking some specific conditions.

        Should add text errors to the list, or raise an exception.
        """
