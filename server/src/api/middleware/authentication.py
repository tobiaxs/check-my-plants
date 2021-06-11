from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.middleware.cookie_scheme import CookieBearer
from src.database.models import User
from src.schemas.jwt_token import JwtTokenEncoded
from src.services.jwt_token import JwtTokenService

http_scheme = HTTPBearer()

cookie_scheme = CookieBearer()


async def token_refresh_middleware(
    token: HTTPAuthorizationCredentials = Depends(http_scheme),
) -> JwtTokenEncoded:
    """Middleware for validating and refreshing jwt token.

    Checks if the token is valid and, depending on the output,
    refreshes it or raises an exception.
    """
    refreshed_token = await JwtTokenService.refresh_jwt(token.dict().get("credentials"))
    return refreshed_token


async def user_middleware(
    token: HTTPAuthorizationCredentials = Depends(http_scheme),
) -> User:
    """Middleware for validating and decoding jwt token from header.

    Retrieves and returns a User instance from token payload if it's correct,
    otherwise raises an exception.
    """
    decoded_token = JwtTokenService.decode_jwt(token.dict().get("credentials"))
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token is either wrong or expired")
    user = await JwtTokenService.get_user_from_token(decoded_token)
    return user


async def cookie_user_middleware(
    token: Optional[HTTPAuthorizationCredentials] = Depends(cookie_scheme),
) -> Optional[User]:
    """Retrieves user instance from jwt token if it's correct,
    otherwise returns none.
    """
    if not token:
        return None
    decoded_token = JwtTokenService.decode_jwt(token.credentials)
    if not decoded_token:
        return None
    user = await JwtTokenService.get_user_from_token(decoded_token)
    return user
