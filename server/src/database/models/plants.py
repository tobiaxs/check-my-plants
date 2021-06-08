from tortoise import fields

from src.database.models.enums import Conditions
from src.database.models.generic import GenericModel


class Plant(GenericModel):
    """Model for storing plants data."""

    name = fields.CharField(max_length=63)
    description = fields.TextField()
    temperature = fields.CharEnumField(Conditions)
    humidity = fields.CharEnumField(Conditions)
    is_accepted = fields.BooleanField(default=False)

    """Relational fields."""
    creator = fields.ForeignKeyField(
        "models.User", related_name="plants", on_delete=fields.CASCADE
    )
    # TODO: Category, Image
