from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request


class CookieBearer(HTTPBearer):
    """Scheme for in-cookie optional jwt token."""

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        """Looks for jwt token in cookie and returns it or returns none."""
        access_token: str = request.cookies.get("access_token")
        scheme, credentials = get_authorization_scheme_param(access_token)
        if not all((access_token, scheme, credentials)) or scheme.lower() != "bearer":
            return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
