from pydantic import BaseModel, EmailStr


class JwtTokenEncoded(BaseModel):
    """Base jwt token schema."""

    access_token: str


class JwtTokenDecoded(BaseModel):
    """Payload from decoded jwt token."""

    email: EmailStr
    expires: float
