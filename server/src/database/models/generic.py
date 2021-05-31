from abc import ABCMeta

from tortoise import fields, models


class GenericModel(models.Model):
    """Class containing generic fields."""

    __metaclass__ = ABCMeta

    uuid = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
