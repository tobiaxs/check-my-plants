from fastapi import APIRouter

from src.database.crud.users import authenticate_user, create_user
from src.schemas.jwt_token import JwtTokenEncoded
from src.schemas.users import UserPayload

router = APIRouter()


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
