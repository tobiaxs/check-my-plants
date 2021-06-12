from abc import ABC, abstractmethod


class GenericValidator(ABC):
    """Interface for form validators."""

    def __init__(self):
        self.errors: list[str] = []

    @abstractmethod
    def validate(self, data: dict):
        raise NotImplementedError()
