import uuid

import pytest
from httpx import AsyncClient

from src.database.models import Plant, User
from src.database.models.enums import Conditions
from tests.conftest import TEST_USER_EMAIL

PLANT_PAYLOAD = {
    "name": "Some Plant",
    "description": "Some Description about Some Plant",
    "temperature": Conditions.low.value,
    "humidity": Conditions.high.value,
}

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
    for plant_payload in PLANTS_PAYLOAD:
        # TODO: is_accepted has to be true
        await Plant.create(
            **plant_payload,
            creator=await User.get(email=TEST_USER_EMAIL),
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
    # TODO: is_accepted has to be true
    plant = await Plant.create(
        **PLANT_PAYLOAD,
        creator=await User.get(email=TEST_USER_EMAIL),
        is_accepted=False,
    )

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
    response = await cookie_client.post("/plant/create", data=PLANT_PAYLOAD)
    content = response.content.decode()

    detail_view_text = f"Created by {TEST_USER_EMAIL}"
    plant = await Plant.get_or_none(name=PLANT_PAYLOAD["name"])

    assert response.status_code == 200
    assert detail_view_text in content
    assert plant is not None
    await plant.fetch_related("creator")
    assert plant.creator.email == TEST_USER_EMAIL


async def test_plant_create_no_user(client: AsyncClient):
    """Test plant create form with no user cookie."""
    response = await client.post("/plant/create", data=PLANT_PAYLOAD)
    content = response.content.decode()

    error_text = "You are not permitted to visit this page"
    plant = await Plant.get_or_none(name=PLANT_PAYLOAD["name"])

    assert response.status_code == 403
    assert error_text in content
    assert plant is None


async def test_plant_create_wrong_cookie(cookie_client: AsyncClient):
    """Test plant create form with wrong user cookie."""
    cookie_client.cookies = {"access_token": "Bearer very very wrong"}
    response = await cookie_client.post("/plant/create", data=PLANT_PAYLOAD)
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
    response = await cookie_client.post("/plant/create", data=payload)
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
