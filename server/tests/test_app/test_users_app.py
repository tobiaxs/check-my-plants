import uuid

import pytest
from httpx import AsyncClient
from pydantic import SecretStr

from src.database.models import Image, Plant, User
from src.database.models.enums import Conditions
from src.services.hashing import HashingService
from tests.conftest import TEST_USER_EMAIL

PLANT_PAYLOAD = {
    "name": "Some Plant",
    "description": "Some Description about Some Plant",
    "temperature": Conditions.low,
    "humidity": Conditions.high,
}

USER_PAYLOAD = {
    "email": "some@user.com",
    "password": "some-password",
    "password_confirm": "some-password",
}

PASSWORD_PAYLOAD = {
    "old_password": "pytest-auth-user",
    "password": "newpassword",
    "password_confirm": "newpassword",
}

pytestmark = [pytest.mark.asyncio]


async def test_register_route(client: AsyncClient):
    """Checks route with user register form."""
    response = await client.get("/register")
    register_unique_text = "Already have an account?"

    assert response.status_code == 200
    assert register_unique_text in str(response.content)


async def test_register_route_with_user(cookie_client: AsyncClient):
    """Checks if request gets redirected as user is already logged in.

    Plant is additionally created to make dashboard not empty.
    """
    # TODO: is_accepted has to be true
    await Plant.create(
        **PLANT_PAYLOAD,
        creator=await User.get(email=TEST_USER_EMAIL),
        image=await Image.create(name="some_name.jpg", path="some/path"),
        is_accepted=False,
    )

    response = await cookie_client.get("/register")
    content = str(response.content)
    register_unique_text = "Already have an account?"
    dashboard_unique_text = "Check this plant"

    assert response.status_code == 200
    assert register_unique_text not in content
    assert dashboard_unique_text in content


async def test_register_form(client: AsyncClient):
    """Checks registering user using form with correct payload."""
    response = await client.post("/register", data=USER_PAYLOAD)
    register_message = "You can now login into our app"

    assert response.status_code == 201
    assert register_message in str(response.content)
    assert await User.get_or_none(email=USER_PAYLOAD["email"])


async def test_register_form_too_short_errors(client: AsyncClient):
    """Checks registering user using form with wrong payload."""
    payload = {
        "email": "short",
        "password": "short",
        "password_confirm": "notevenmatching",
    }
    response = await client.post("/register", data=payload)
    content = str(response.content)

    email_error = "Email address is too short"
    password_error = "Password is too short"
    password_confirm_error = "Passwords didn't match".replace("'", "&#39;")

    assert response.status_code == 422
    assert email_error in content
    assert password_error in content
    assert password_confirm_error in content
    assert not await User.get_or_none(email=USER_PAYLOAD["email"])


async def test_register_form_too_long_errors(client: AsyncClient):
    """Checks registering user using form with wrong payload."""
    long_string = "very-very-long" * 10
    payload = {
        "email": long_string,
        "password": long_string,
        "password_confirm": long_string,
    }
    response = await client.post("/register", data=payload)
    content = str(response.content)

    email_error = "Email address is too long"
    password_error = "Password is too long"

    assert response.status_code == 422
    assert email_error in content
    assert password_error in content
    assert await User.all().count() == 0


async def test_register_form_existing_user(client: AsyncClient):
    """Checks registering user using form with already existing user."""
    await User.create(**USER_PAYLOAD, hashed_password=USER_PAYLOAD["password"])
    response = await client.post("/register", data=USER_PAYLOAD)
    content = str(response.content)

    user_error = "User with that email already exists"

    assert response.status_code == 422
    assert user_error in content
    assert await User.all().count() == 1


async def test_login_route(client: AsyncClient):
    """Checks route with user login form."""
    response = await client.get("/login")
    login_unique_text = "Don't have an account?"

    assert response.status_code == 200
    assert login_unique_text in response.content.decode()


async def test_login_route_with_user(cookie_client: AsyncClient):
    """Checks if request gets redirected as user is already logged in.

    Plant is additionally created to make dashboard not empty.
    """
    # TODO: is_accepted has to be true
    await Plant.create(
        **PLANT_PAYLOAD,
        creator=await User.get(email=TEST_USER_EMAIL),
        image=await Image.create(name="some_name.jpg", path="some/path"),
        is_accepted=False,
    )

    response = await cookie_client.get("/login")
    content = response.content.decode()
    login_unique_text = "Don't have an account?"
    dashboard_unique_text = "Check this plant"

    assert response.status_code == 200
    assert login_unique_text not in content
    assert dashboard_unique_text in content


async def test_login_form(client: AsyncClient):
    """Checks logging user in using form with correct payload.

    Plant is additionally created to make dashboard not empty.
    """
    instance_payload = {
        "email": USER_PAYLOAD["email"],
        "hashed_password": HashingService.get_hashed_password(
            SecretStr(USER_PAYLOAD["password"])
        ),
    }
    user = await User.create(**instance_payload)
    # TODO: is_accepted has to be true
    await Plant.create(
        **PLANT_PAYLOAD,
        creator=user,
        image=await Image.create(name="some_name.jpg", path="some/path"),
        is_accepted=False,
    )

    response = await client.post("/login", data=USER_PAYLOAD)
    content = response.content.decode()
    login_unique_text = "Don't have an account?"
    dashboard_unique_text = "Check this plant"

    assert response.status_code == 200
    assert login_unique_text not in content
    assert dashboard_unique_text in content


async def test_login_form_not_existing_user(client: AsyncClient):
    """Checks logging user in using form with not existing user."""
    response = await client.post("/login", data=USER_PAYLOAD)
    content = response.content.decode()

    user_error = "User with that email does not exist"

    assert response.status_code == 422
    assert user_error in content


async def test_login_form_wrong_password(client: AsyncClient):
    """Checks logging user in using form with not existing user."""
    instance_payload = {
        "email": USER_PAYLOAD["email"],
        "hashed_password": HashingService.get_hashed_password(
            SecretStr("different-password")
        ),
    }
    await User.create(**instance_payload)
    response = await client.post("/login", data=USER_PAYLOAD)
    content = response.content.decode()

    user_error = "Password you have entered is not correct"

    assert response.status_code == 422
    assert user_error in content


async def test_logout(cookie_client: AsyncClient):
    """Checks user logout view."""
    response = await cookie_client.get("/logout")
    content = response.content.decode()

    logout_message = "You have been logged out successfully"

    assert response.status_code == 200
    assert logout_message in content
    assert response.cookies == {}


async def test_user_profile(cookie_client: AsyncClient):
    """Checks user profile view."""
    user = await User.get(email=TEST_USER_EMAIL)
    response = await cookie_client.get(f"/profile/{user.pk}")
    content = response.content.decode()

    assert response.status_code == 200
    assert user.email in content


async def test_user_profile_no_user(client: AsyncClient):
    """Checks user profile view with wrong user uuid."""
    response = await client.get(f"/profile/{uuid.uuid4()}")
    content = response.content.decode()

    assert response.status_code == 404
    assert "The page you tried to access does not exist" in content


async def test_user_delete(cookie_client: AsyncClient):
    """Checks user delete view."""
    user = await User.get(email=TEST_USER_EMAIL)
    response = await cookie_client.post(f"/profile/{user.pk}")
    content = response.content.decode()

    delete_message = "User has been deleted successfully."

    assert response.status_code == 200
    assert delete_message in content
    assert not await User.get_or_none(email=TEST_USER_EMAIL)


async def test_user_delete_no_user(client: AsyncClient):
    """Checks user delete view with no user."""
    response = await client.post(f"/profile/{uuid.uuid4()}")
    content = response.content.decode()

    assert response.status_code == 404
    assert "The page you tried to access does not exist" in content


async def test_user_delete_wrong_user(cookie_client: AsyncClient):
    """Checks user delete view with wrong user."""
    profile_user = await User.create(
        **USER_PAYLOAD, hashed_password=USER_PAYLOAD["password"]
    )
    response = await cookie_client.post(f"/profile/{profile_user.pk}")
    content = response.content.decode()

    error_text = "You are not permitted to visit this page"

    assert response.status_code == 403
    assert error_text in content


async def test_change_password_form(cookie_client: AsyncClient):
    """Checks displaying user password form."""
    user = await User.get(email=TEST_USER_EMAIL)
    response = await cookie_client.get(f"/change_password/{user.pk}")
    content = response.content.decode()

    form_message = "Change your password"

    assert response.status_code == 200
    assert form_message in content


async def test_change_password_form_no_user(client: AsyncClient):
    """Checks displaying user password form for no user."""
    response = await client.get(f"/change_password/{uuid.uuid4()}")
    content = response.content.decode()

    assert response.status_code == 404
    assert "The page you tried to access does not exist" in content


async def test_change_password_form_wrong_user(cookie_client: AsyncClient):
    """Checks displaying user password form for wrong user."""
    profile_user = await User.create(
        **USER_PAYLOAD, hashed_password=USER_PAYLOAD["password"]
    )
    response = await cookie_client.get(f"/change_password/{profile_user.pk}")
    content = response.content.decode()

    error_text = "You are not permitted to visit this page"

    assert response.status_code == 403
    assert error_text in content


async def test_change_password(cookie_client: AsyncClient):
    """Checks changing password for correct user."""
    user = await User.get(email=TEST_USER_EMAIL)
    response = await cookie_client.post(
        f"/change_password/{user.pk}", data=PASSWORD_PAYLOAD
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert "Password has been changed successfully!" in content
    await user.refresh_from_db()
    assert HashingService.verify_password(
        SecretStr(PASSWORD_PAYLOAD["password"]), user.hashed_password
    )


async def test_change_password_no_user(client: AsyncClient):
    """Checks changing user password for no user."""
    response = await client.post(
        f"/change_password/{uuid.uuid4()}", data=PASSWORD_PAYLOAD
    )
    content = response.content.decode()

    assert response.status_code == 404
    assert "The page you tried to access does not exist" in content


async def test_change_password_wrong_user(cookie_client: AsyncClient):
    """Checks changing user password for wrong user."""
    profile_user = await User.create(
        **USER_PAYLOAD, hashed_password=USER_PAYLOAD["password"]
    )
    response = await cookie_client.post(
        f"/change_password/{profile_user.pk}", data=PASSWORD_PAYLOAD
    )
    content = response.content.decode()

    error_text = "You are not permitted to visit this page"

    assert response.status_code == 403
    assert error_text in content


async def test_change_password_errors(cookie_client: AsyncClient):
    """Checks changing password for correct user with wrong payload."""
    user = await User.get(email=TEST_USER_EMAIL)
    payload = {
        "old_password": "absolutely-wrong",
        "password": "shorty",
        "password_confirm": "dont-match",
    }
    response = await cookie_client.post(f"/change_password/{user.pk}", data=payload)
    content = response.content.decode()

    assert response.status_code == 422
    assert "Password you have entered is not correct" in content
    assert "Passwords didn't match".replace("'", "&#39;") in content
    await user.refresh_from_db()
    assert not HashingService.verify_password(
        SecretStr(PASSWORD_PAYLOAD["password"]), user.hashed_password
    )
