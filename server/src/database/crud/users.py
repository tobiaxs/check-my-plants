from fastapi import HTTPException

from src.database.models.users import User
from src.schemas.users import JwtTokenEncoded, UserCreate
from src.services.hashing import HashingService
from src.services.jwt_token import JwtTokenService


async def create_user(payload: UserCreate) -> JwtTokenEncoded:
    """Creates a new user."""
    existing_user = await User.get_or_none(email=payload.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    user = await User.create(
        email=payload.email,
        hashed_password=HashingService.get_hashed_password(payload.password),
    )
    token = JwtTokenService.encode_jwt(user.email)
    return token
