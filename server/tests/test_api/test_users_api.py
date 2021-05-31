import json

import pytest
from httpx import AsyncClient

from src.services.jwt_token import JwtTokenService

pytestmark = [pytest.mark.asyncio]


async def test_create_user(client: AsyncClient):
    """Checks User creation."""
    payload = {"email": "peter.tobias@gmail.com", "password": "mypassword.."}
    response = await client.post("/users/register", data=json.dumps(payload))
    data = response.json()

    assert response.status_code == 201
    decoded_token = JwtTokenService.decode_jwt(data.get("access_token"))
    assert decoded_token.dict().get("email") == payload.get("email")
