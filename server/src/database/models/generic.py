from abc import ABCMeta

from tortoise import fields, models


class GenericModel(models.Model):
    """Abstract class containing generic fields."""

    __metaclass__ = ABCMeta

    uuid = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
