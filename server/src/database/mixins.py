from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class SaveModelMixin:
    """Mixin for save functionality."""

    async def save(self, session: AsyncSession) -> None:
        """Saves the object."""
        try:
            session.add(self)
            return await session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex))


class DeleteModelMixin:
    """Mixin for delete functionality."""

    async def delete(self, session: AsyncSession) -> None:
        """Deletes the object."""
        try:
            await session.delete(self)
            await session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex))


class RetrieveModelMixin:
    """Mixin for get functionality."""

    @classmethod
    async def get_by_field(cls, field: str, value: Any, session: AsyncSession) -> "RetrieveModelMixin":
        """Creates the query for specific class based on field and value,
        searches for the object and returns the result.
        """
        query = select(cls).where(getattr(cls, field) == value)
        result = await session.execute(query)
        instance = result.scalars().first()
        return instance


class BaseModelMixin(SaveModelMixin, DeleteModelMixin, RetrieveModelMixin):
    """Mixin for adding get, save and delete functionalities to the base model."""
