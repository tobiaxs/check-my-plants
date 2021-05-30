from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import User
from src.schemas.users import JwtTokenEncoded, UserCreate
from src.services.hashing import HashingService
from src.services.jwt_token import JwtTokenService


async def create_user(payload: UserCreate, session: AsyncSession) -> JwtTokenEncoded:
    """Creates a new user."""
    existing_user = await User.get_by_field("email", payload.email, session)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    user = User(
        email=payload.email,
        hashed_password=HashingService.get_hashed_password(payload.password),
    )
    await user.save(session)
    token = JwtTokenService.encode_jwt(user.email)
    return token
