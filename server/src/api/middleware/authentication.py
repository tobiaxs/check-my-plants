from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.database.models import User
from src.schemas.jwt_token import JwtTokenEncoded
from src.services.jwt_token import JwtTokenService

http_scheme = HTTPBearer()


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
    """Middleware for validating and decoding jwt token.

    Retrieves and returns a User instance from token payload if it's correct,
    otherwise raises an exception.
    """
    decoded_token = JwtTokenService.decode_jwt(token.dict().get("credentials"))
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token is either wrong or expired")
    user = await JwtTokenService.get_user_from_token(decoded_token)
    return user
