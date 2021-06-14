from fastapi import APIRouter, Depends

from src.api.middleware.authentication import token_refresh_middleware
from src.database.crud.users import authenticate_user, create_user
from src.schemas.jwt_token import JwtTokenEncoded
from src.schemas.users import UserPayload

router = APIRouter(prefix="/api/users", tags=["Users Api"])


@router.post("/register", status_code=201, response_model=JwtTokenEncoded)
async def register(payload: UserPayload) -> JwtTokenEncoded:
    """Creates a user instance and returns a response with an access token."""
    token = await create_user(payload)
    return token


@router.post("/login", response_model=JwtTokenEncoded)
async def login(payload: UserPayload) -> JwtTokenEncoded:
    """Given user credentials, creates and returns a new access token."""
    token = await authenticate_user(payload)
    return token


@router.get("/refresh", response_model=JwtTokenEncoded)
async def refresh(
    token: JwtTokenEncoded = Depends(token_refresh_middleware),
) -> JwtTokenEncoded:
    """Checks if the token is valid and refreshes it."""
    return token
