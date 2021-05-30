from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud.users import create_user
from src.database.session import get_db
from src.schemas.users import JwtTokenEncoded, UserCreate

router = APIRouter()


@router.post("/register", status_code=201, response_model=JwtTokenEncoded)
async def register(
    payload: UserCreate, session: AsyncSession = Depends(get_db)
) -> JwtTokenEncoded:
    """Creates a User instance and returns a response with access token."""
    token = await create_user(payload, session)
    return token
