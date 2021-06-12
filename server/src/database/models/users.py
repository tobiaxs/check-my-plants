from tortoise import fields

from src.database.models.generic import GenericModel


class User(GenericModel):
    """Model for storing users data."""

    email = fields.CharField(max_length=127, unique=True)
    hashed_password = fields.CharField(max_length=127)
    is_superuser = fields.BooleanField(default=False)

    # TODO: Nickname, Profile Picture, Is Active
