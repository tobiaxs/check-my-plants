from sqlalchemy import Column, String, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base_class import Base
from src.database.models.enums import Conditions


class Plant(Base):
    """Class for storing plants data."""

    __tablename__ = "plants"

    name = Column(String(63), nullable=False)
    description = Column(String, nullable=False)
    temperature = Column(Enum(Conditions), nullable=False)
    humidity = Column(Enum(Conditions), nullable=False)
    is_accepted = Column(Boolean, default=True)

    """Relation fields."""
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    creator = relationship("User", back_populates="plants")
