from fastapi import HTTPException

from src.api.forms.validators.generic import GenericValidator
from src.database.models.enums import Conditions


class NameLengthValidator(GenericValidator):
    def validate(self, data: dict) -> None:
        """Checks the name length."""
        if len(data["name"]) > 127:
            self.errors.append("Name is too long")


class CreatorValidator(GenericValidator):
    def validate(self, data: dict) -> None:
        """If creator is not in the payload, 403 should be raised immediately."""
        if not data["creator"]:
            raise HTTPException(
                status_code=403, detail="You are not allowed to perform this action"
            )


class ConditionsValidator(GenericValidator):
    def validate(self, data: dict) -> None:
        """Checks if given values are in conditions enum."""
        if not data["temperature"] in Conditions.__members__:
            self.errors.append("Wrong temperature value")
        if not data["humidity"] in Conditions.__members__:
            self.errors.append("Wrong humidity value")
