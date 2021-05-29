import os
import time
from typing import Optional

from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.database.session import get_db
from src.schemas.users import JwtTokenEncoded, JwtTokenDecoded

JWT_SECRET = os.getenv("SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")


class JwtTokenService:
    """Service for controlling jwt tokens flow."""

    @staticmethod
    def encode_jwt(email: str) -> JwtTokenEncoded:
        """Returns valid jwt token based on given email."""
        payload = {"email": email, "expires": time.time() + 600}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return JwtTokenEncoded.parse_obj({"access_token": token})

    @staticmethod
    def decode_jwt(token: str) -> Optional[JwtTokenDecoded]:
        """Checks if given token is valid and not expired and returns its payload."""
        try:
            decoded_token = jwt.decode(
                token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
            )
            return (
                JwtTokenDecoded.parse_obj(decoded_token)
                if decoded_token["expires"] >= time.time()
                else None
            )
        except JWTError:
            return None

    @classmethod
    async def refresh_jwt(cls, token: str) -> JwtTokenEncoded:
        """Decodes given token, checks its validity and returns new, refreshed token."""
        decoded_token = cls.decode_jwt(token)
        if not decoded_token:
            raise HTTPException(status_code=401, detail="Token is either wrong or expired")
        user = await cls.get_user_from_token(decoded_token)
        refreshed_token = cls.encode_jwt(user.email)
        return refreshed_token

    @staticmethod
    async def get_user_from_token(decoded_token: JwtTokenDecoded, session: AsyncSession = Depends(get_db)) -> User:
        """Checks token validity and raises an exception if it's not valid.
        If payload matches all requirements, User instance is getting returned.
        """
        user = await User.get_by_field("email", decoded_token.email, session)
        if not user:
            raise HTTPException(status_code=401, detail="User from token payload does not exist")
        return user
