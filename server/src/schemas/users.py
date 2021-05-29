from pydantic import BaseModel, EmailStr, SecretStr


class UserCreate(BaseModel):
    """Payload needed for User creation."""

    email: EmailStr
    password: SecretStr


class JwtTokenEncoded(BaseModel):
    """Base jwt token schema."""

    access_token: str


class JwtTokenDecoded(BaseModel):
    """Payload from decoded jwt token."""

    email: EmailStr
    expires: float
