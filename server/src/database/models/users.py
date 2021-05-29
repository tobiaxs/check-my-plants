from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from src.database.base_class import Base


class User(Base):
    """Class for storing users data."""

    __tablename__ = "users"

    email = Column(EmailType, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

    """Relation fields."""
    plants = relationship("Plant", back_populates="creator")
