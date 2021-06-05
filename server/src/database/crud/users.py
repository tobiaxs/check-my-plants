from fastapi import HTTPException

from src.database.models.users import User
from src.schemas.jwt_token import JwtTokenEncoded
from src.schemas.users import UserPayload
from src.services.hashing import HashingService
from src.services.jwt_token import JwtTokenService


async def create_user(payload: UserPayload) -> JwtTokenEncoded:
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


async def authenticate_user(payload: UserPayload) -> JwtTokenEncoded:
    """Creates and returns a new access token."""
    user = await User.get_or_none(email=payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    if not HashingService.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong email or password")
    return JwtTokenService.encode_jwt(user.email)
