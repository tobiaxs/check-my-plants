import inspect
from abc import ABCMeta
from datetime import datetime
from typing import Type
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel


class BaseOrmModel(BaseModel):
    """Schema containing fields from generic model."""

    __metaclass__ = ABCMeta

    uuid: UUID
    created_at: datetime

    class Config:
        orm_mode = True


def as_form(cls: Type[BaseModel]) -> Type[BaseModel]:
    """Adds an as_form class method to decorated models.
    It allows whole payload to be send along the request files.
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
            annotation=field.outer_type_,
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls
