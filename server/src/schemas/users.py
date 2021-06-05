from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr


class UserPayload(BaseModel):
    """Payload needed for User creation."""

    email: EmailStr
    password: SecretStr


class UserModelUuid(BaseModel):
    """Payload containing only uuid of user instance."""

    uuid: UUID

    class Config:
        orm_mode = True
