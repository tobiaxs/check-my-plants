import json

import pytest
from httpx import AsyncClient

from src.database.models import User
from src.services.jwt_token import JwtTokenService

pytestmark = [pytest.mark.asyncio]


async def test_create_user(client: AsyncClient):
    """Checks user creation."""
    payload = {"email": "peter.tobias@gmail.com", "password": "mypassword.."}
    response = await client.post("/users/register", data=json.dumps(payload))
    data = response.json()

    assert response.status_code == 201
    decoded_token = JwtTokenService.decode_jwt(data.get("access_token"))
    assert decoded_token.dict().get("email") == payload.get("email")
    assert await User.all().count() == 1


async def test_create_user_with_existing_user(client: AsyncClient):
    """Checks if 400 is raised after trying to create already existing user."""
    model_payload = {
        "email": "jon.jones@gmail.com",
        "hashed_password": "unhashed but whatever",
    }
    post_payload = {"email": "jon.jones@gmail.com", "password": "unhashed but whatever"}
    await User.create(**model_payload)
    response = await client.post("/users/register", data=json.dumps(post_payload))

    assert response.status_code == 400
    assert response.json().get("detail") == "User with this email already exists"
    assert await User.all().count() == 1
