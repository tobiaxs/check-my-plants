from fastapi import APIRouter

from src.database.crud.users import create_user
from src.schemas.users import JwtTokenEncoded, UserCreate

router = APIRouter()


@router.post("/register", status_code=201, response_model=JwtTokenEncoded)
async def register(payload: UserCreate) -> JwtTokenEncoded:
    """Creates a User instance and returns a response with access token."""
    token = await create_user(payload)
    return token
