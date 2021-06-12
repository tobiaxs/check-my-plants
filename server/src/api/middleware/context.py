from typing import Optional

from fastapi import Depends
from starlette.requests import Request

from src.api.middleware.authentication import cookie_user_middleware
from src.database.models import User


def context_middleware(
    request: Request, cookie_user: Optional[User] = Depends(cookie_user_middleware)
) -> dict:
    """Builds a default context with optional user coming from the cookie."""
    return {"request": request, "user": cookie_user}
