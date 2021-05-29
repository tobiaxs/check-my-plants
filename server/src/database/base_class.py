from uuid import uuid4

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import as_declarative

from src.database.mixins import BaseModelMixin


@as_declarative()
class Base(BaseModelMixin):
    """Base class for constructing orm models."""

    __tablename__: str

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    created_at = Column(DateTime(timezone=True), default=func.now())

    def __init__(self, *args, **kwargs):
        """Fixes the inspections."""
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        """Returns string representation."""
        return str(self)

    def __str__(self) -> str:
        """Returns the class name with object id."""
        return f"<{self.__class__.__name__} object with id={self.id}>"
