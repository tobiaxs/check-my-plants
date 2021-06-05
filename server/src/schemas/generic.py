from abc import ABCMeta
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseOrmModel(BaseModel):
    """Schema containing fields from generic model."""

    __metaclass__ = ABCMeta

    uuid: UUID
    created_at: datetime

    class Config:
        orm_mode = True
