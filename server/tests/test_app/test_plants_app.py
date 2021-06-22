import uuid

import pytest
from httpx import AsyncClient

from src.database.models import Image, Plant, User
from src.database.models.enums import Conditions
from tests.conftest import TEST_USER_EMAIL
from tests.test_api.test_plants_api import (
    TEST_FILE,
    check_all_fields,
    create_test_plant_instances,
)
from tests.test_app.test_users_app import USER_PAYLOAD

PLANT_PAYLOAD = {
    "name": "Some Plant",
    "description": "Some Description about Some Plant",
    "temperature": Conditions.low.value,
    "humidity": Conditions.high.value,
}

PLANT_EDIT_PAYLOAD = {
    "name": "New Plant",
    "description": "New Description about New Plant",
    "temperature": Conditions.high.value,
    "humidity": Conditions.low.value,
}

EMPTY_FILE = {"image": (".", bytes(), "image/jpeg")}

PLANTS_PAYLOAD = [
    PLANT_PAYLOAD,
    {
        "name": "Another Plant",
        "description": "Some Description about Another Plant",
        "temperature": Conditions.average,
        "humidity": Conditions.average,
    },
]

pytestmark = [pytest.mark.asyncio]


async def test_plants_dashboard(cookie_client: AsyncClient):
    """Tests plants dashboard route."""
    user = await User.get(email=TEST_USER_EMAIL)
    for plant_payload in PLANTS_PAYLOAD:
        # TODO: is_accepted has to be true
        image = await Image.create(name="some_name.jpg", path="some/path")
        await Plant.create(
            **plant_payload,
            creator=user,
            image=image,
            is_accepted=False,
        )

    response = await cookie_client.get("/")
    content = response.content.decode()
    dashboard_unique_text = "Check this plant"

    assert response.status_code == 200
    assert dashboard_unique_text in content
    for plant in PLANTS_PAYLOAD:
        assert plant["name"] in content


async def test_plant_details(cookie_client: AsyncClient):
    """Tests plant details route."""
    _, _, plant = await create_test_plant_instances()

    response = await cookie_client.get(f"/plants/{plant.uuid}")
    content = response.content.decode()

    assert response.status_code == 200
    assert plant.name in content


async def test_plant_details_not_existing_plant(cookie_client: AsyncClient):
    """Tests plant details route for not existing plant."""
    response = await cookie_client.get(f"/plants/{uuid.uuid4()}")
    content = response.content.decode()

    assert response.status_code == 404
    assert "The page you tried to access does not exist" in content


async def test_plant_create_form_route(cookie_client: AsyncClient):
    """Tests displaying plant create form."""
    response = await cookie_client.get("/plant/create")
    content = response.content.decode()

    form_text = "Create a new plant"

    assert response.status_code == 200
    assert form_text in content


async def test_plant_create_form_route_no_user(client: AsyncClient):
    """Tests receiving 403 response when user is not logged in."""
    response = await client.get("/plant/create")
    content = response.content.decode()

    error_text = "You are not permitted to visit this page"

    assert response.status_code == 403
    assert error_text in content


async def test_plant_create(cookie_client: AsyncClient):
    """Test plant create form with correct payload."""
    response = await cookie_client.post(
        "/plant/create", data=PLANT_PAYLOAD, files=TEST_FILE
    )
    content = response.content.decode()

    detail_view_text = TEST_USER_EMAIL
    plant = await Plant.get_or_none(name=PLANT_PAYLOAD["name"])

    assert response.status_code == 200
    assert detail_view_text in content
    assert plant is not None
    await plant.fetch_related("creator")
    assert plant.creator.email == TEST_USER_EMAIL


async def test_plant_create_no_user(client: AsyncClient):
    """Test plant create form with no user cookie."""
    response = await client.post("/plant/create", data=PLANT_PAYLOAD, files=TEST_FILE)
    content = response.content.decode()

    error_text = "You are not permitted to visit this page"
    plant = await Plant.get_or_none(name=PLANT_PAYLOAD["name"])

    assert response.status_code == 403
    assert error_text in content
    assert plant is None


async def test_plant_create_wrong_cookie(cookie_client: AsyncClient):
    """Test plant create form with wrong user cookie."""
    cookie_client.cookies = {"access_token": "Bearer very very wrong"}
    response = await cookie_client.post(
        "/plant/create", data=PLANT_PAYLOAD, files=TEST_FILE
    )
    content = response.content.decode()

    error_text = "You are not permitted to visit this page"
    plant = await Plant.get_or_none(name=PLANT_PAYLOAD["name"])

    assert response.status_code == 403
    assert error_text in content
    assert plant is None


async def test_plant_create_wrong_payload(cookie_client: AsyncClient):
    """Test plant create form with no too long name and wrong enums."""
    payload = {
        "name": "toolongname" * 15,
        "description": "icantfailbtw",
        "temperature": "wrong",
        "humidity": "wrongtoo",
    }
    response = await cookie_client.post("/plant/create", data=payload, files=TEST_FILE)
    content = response.content.decode()

    name_error = "Name is too long"
    temperature_error = "Wrong temperature value"
    humidity_error = "Wrong humidity value"
    plant = await Plant.get_or_none(name=PLANT_PAYLOAD["name"])

    assert response.status_code == 422
    assert name_error in content
    assert temperature_error in content
    assert humidity_error in content
    assert plant is None


async def test_plant_delete(cookie_client: AsyncClient):
    """Tests deleting plant."""
    user = await User.get(email=TEST_USER_EMAIL)
    image = await Image.create(name="some_name.jpg", path="some/path")
    plant = await Plant.create(**PLANT_PAYLOAD, creator=user, image=image)

    response = await cookie_client.post(f"/plant/delete/{plant.pk}")
    content = response.content.decode()

    assert response.status_code == 200
    assert "Plant has been deleted successfully" in content


async def test_plant_delete_no_plant(cookie_client: AsyncClient):
    """Tests deleting not existing plant."""
    response = await cookie_client.post(f"/plant/delete/{uuid.uuid4()}")
    content = response.content.decode()

    assert response.status_code == 404
    assert "The page you tried to access does not exist" in content


async def test_plant_delete_wrong_user(cookie_client: AsyncClient):
    """Tests deleting plant user that is not an creator."""
    user = await User.create(**USER_PAYLOAD, hashed_password=USER_PAYLOAD["password"])
    image = await Image.create(name="some_name.jpg", path="some/path")
    plant = await Plant.create(**PLANT_PAYLOAD, creator=user, image=image)

    response = await cookie_client.post(f"/plant/delete/{plant.pk}")
    content = response.content.decode()

    assert response.status_code == 403
    assert "You are not permitted to visit this page" in content


async def test_plant_edit_form(cookie_client: AsyncClient):
    """Tests displaying plant edit form."""
    user = await User.get(email=TEST_USER_EMAIL)
    _, _, plant = await create_test_plant_instances(user)

    response = await cookie_client.get(f"/plant/edit/{plant.pk}")
    content = response.content.decode()

    assert response.status_code == 200
    assert "Edit your plant" in content
    assert plant.name in content


async def test_plant_edit_form_no_plant(cookie_client: AsyncClient):
    """Tests displaying plant edit form for not existing plant."""
    response = await cookie_client.get(f"/plant/edit/{uuid.uuid4()}")
    content = response.content.decode()

    assert response.status_code == 404
    assert "The page you tried to access does not exist" in content


async def test_plant_edit_form_wrong_user(cookie_client: AsyncClient):
    """Tests displaying plant edit form for user that is not creator."""
    _, _, plant = await create_test_plant_instances()
    response = await cookie_client.get(f"/plant/edit/{plant.pk}")
    content = response.content.decode()

    assert response.status_code == 403
    assert "You are not permitted to visit this page" in content


async def test_plant_edit(cookie_client: AsyncClient):
    """Tests editing plant."""
    user = await User.get(email=TEST_USER_EMAIL)
    _, image, plant = await create_test_plant_instances(user)

    response = await cookie_client.post(
        f"/plant/edit/{plant.pk}", data=PLANT_EDIT_PAYLOAD, files=EMPTY_FILE
    )
    content = response.content.decode()
    payload = PLANT_EDIT_PAYLOAD.copy()
    payload["image"] = image

    assert response.status_code == 200
    assert "Plant has been edited successfully" in content
    await plant.refresh_from_db()
    await plant.fetch_related("image")
    await check_all_fields(plant, payload, user)


async def test_plant_edit_new_image(cookie_client: AsyncClient):
    """Tests editing plant with new image."""
    user = await User.get(email=TEST_USER_EMAIL)
    _, old_image, plant = await create_test_plant_instances(user)
    new_image_file = {"image": ("very_new_file.jpg", bytes(), "image/jpeg")}

    response = await cookie_client.post(
        f"/plant/edit/{plant.pk}", data=PLANT_EDIT_PAYLOAD, files=new_image_file
    )
    content = response.content.decode()
    payload = PLANT_EDIT_PAYLOAD.copy()
    payload["image"] = await Image.get(name="very_new_file.jpg")

    assert response.status_code == 200
    assert "Plant has been edited successfully" in content
    await plant.refresh_from_db()
    await plant.fetch_related("image")
    assert plant.image != old_image
    await check_all_fields(plant, payload, user)


async def test_plant_edit_wrong_payload(cookie_client: AsyncClient):
    """Tests editing plant with wrong payload."""
    user = await User.get(email=TEST_USER_EMAIL)
    _, _, plant = await create_test_plant_instances(user)
    payload = {
        "name": "toolongname" * 15,
        "description": "icantfailbtw",
        "temperature": "wrong",
        "humidity": "wrongtoo",
    }

    response = await cookie_client.post(
        f"/plant/edit/{plant.pk}", data=payload, files=EMPTY_FILE
    )
    content = response.content.decode()

    assert response.status_code == 422
    assert "Name is too long" in content
    assert "Wrong temperature value" in content
    assert "Wrong humidity value" in content


async def test_plant_edit_no_plant(cookie_client: AsyncClient):
    """Tests editing not existing plant."""
    response = await cookie_client.post(
        f"/plant/edit/{uuid.uuid4()}", data=PLANT_EDIT_PAYLOAD, files=EMPTY_FILE
    )
    content = response.content.decode()

    assert response.status_code == 404
    assert "The page you tried to access does not exist" in content


async def test_plant_edit_wrong_user(cookie_client: AsyncClient):
    """Tests editing plant user that is not an creator."""
    _, _, plant = await create_test_plant_instances()
    response = await cookie_client.post(
        f"/plant/edit/{plant.pk}", data=PLANT_EDIT_PAYLOAD, files=EMPTY_FILE
    )
    content = response.content.decode()

    assert response.status_code == 403
    assert "You are not permitted to visit this page" in content
