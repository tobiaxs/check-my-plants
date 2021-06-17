import uuid
from datetime import datetime
from typing import Optional
from unittest import mock
from unittest.mock import Mock

import pytest
from httpx import AsyncClient

from src.database.models import Image, Plant, User
from src.database.models.enums import Conditions

pytestmark = [pytest.mark.asyncio]

PLANT_PAYLOAD = {
    "name": "Some Plant",
    "description": "Some Description about Some Plant",
    "temperature": Conditions.low.value,
    "humidity": Conditions.high.value,
}
TEST_FILE = {"image": ("some_image.jpg", bytes(), "image/jpeg")}


async def create_test_plant_instances(
    user: Optional[User] = None, image: Optional[Image] = None
) -> tuple[User, Image, Plant]:
    """Creates a user, image and plant instances for testing purposes."""
    # TODO: Replace with factories?
    if not user:
        user, _ = await User.get_or_create(
            email="some@creator.com", hashed_password="created-password"
        )
    if not image:
        image = await Image.create(name="some_name.jpg", path="some/path")
    plant = await Plant.create(
        **PLANT_PAYLOAD, creator=user, image=image, is_accepted=True
    )
    return user, image, plant


async def check_all_fields(
    instance: Plant, payload: dict, user: Optional[User] = None
) -> None:
    """Checks all the fields for given plant instance and payload."""
    if payload.get("uuid"):
        assert str(instance.uuid) == str(payload.pop("uuid"))
    if payload.get("created_at"):
        assert instance.created_at == datetime.fromisoformat(payload.pop("created_at"))
    if payload.get("creator"):
        await check_creator(instance, payload, user)
    for field, value in payload.items():
        assert value == getattr(instance, field)


async def check_creator(
    instance: Plant, payload: dict, user: Optional[User] = None
) -> None:
    """Checks the plants creator.

    Default comes from the fixture.
    """
    if not user:
        user = await User.get(email="pytest@auth.com")
    await instance.fetch_related("creator")
    assert instance.creator.uuid == user.uuid
    assert str(user.uuid) == payload.pop("creator").get("uuid")


async def test_create_plant(auth_client: AsyncClient):
    """Tests plant creation using correct payload."""
    response = await auth_client.post(
        "/api/plants", data=PLANT_PAYLOAD, files=TEST_FILE
    )
    data = response.json()

    assert response.status_code == 201
    assert await Plant.all().count() == 1
    plant = await Plant.get(uuid=data.get("uuid"))
    await check_all_fields(plant, PLANT_PAYLOAD)
    await check_all_fields(plant, data)


async def test_create_plant_wrong_enum(auth_client: AsyncClient):
    """Tests plant creation using wrong enums in payload."""
    payload = PLANT_PAYLOAD.copy()
    payload["temperature"] = "wrong temperature"
    payload["humidity"] = "wrong humidity"

    response = await auth_client.post("/api/plants", data=payload, files=TEST_FILE)
    data = response.json()

    assert response.status_code == 422
    assert await Plant.all().count() == 0
    msg = "value is not a valid enumeration member; permitted: 'low', 'average', 'high'"
    for error in data.get("detail"):
        assert error["msg"] == msg


async def test_create_plant_no_user(client: AsyncClient):
    """Tests plant creation with no user token in the payload."""
    response = await client.post("/api/plants", data=PLANT_PAYLOAD, files=TEST_FILE)

    assert response.status_code == 403
    assert await Plant.all().count() == 0


async def test_create_plant_wrong_token(auth_client: AsyncClient):
    """Tests plant creation with wrong token header."""
    auth_client.headers["Authorization"] = "Bearer very very wrong token"
    response = await auth_client.post(
        "/api/plants", data=PLANT_PAYLOAD, files=TEST_FILE
    )

    assert response.status_code == 401
    assert await Plant.all().count() == 0


async def test_plants_list(client: AsyncClient):
    """Tests retrieving list of plants."""
    plants = [(await create_test_plant_instances())[2] for _ in range(3)]
    user = await User.get(email="some@creator.com")
    response = await client.get("/api/plants")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    for plant_instance, plant_response in zip(plants, data):
        await check_all_fields(plant_instance, plant_response, user)


async def test_plant_retrieve(client: AsyncClient):
    """Tests retrieving specific plant."""
    user, _, plant = await create_test_plant_instances()
    response = await client.get(f"/api/plants/{plant.uuid}")
    data = response.json()

    assert response.status_code == 200
    await check_all_fields(plant, data, user)


async def test_plant_retrieve_wrong_pk(client: AsyncClient):
    """Tests retrieving not existing plant."""
    response = await client.get(f"/api/plants/{uuid.uuid4()}")
    assert response.status_code == 404


@mock.patch("src.database.models.images.shutil.which", return_value=True)
@mock.patch("src.database.models.images.shutil.rmtree")
async def test_plant_delete(
    mock_which: Mock, mock_rmtree: Mock, auth_client: AsyncClient
):
    """Tests deleting plant."""
    user = await User.get(email="pytest@auth.com")
    _, _, plant = await create_test_plant_instances(user=user)
    response = await auth_client.delete(f"/api/plants/{plant.uuid}")

    assert response.status_code == 200
    assert await Plant.all().count() == 0
    assert await Image.all().count() == 0


async def test_plant_delete_wrong_pk(auth_client: AsyncClient):
    """Tests retrieving not existing plant."""
    response = await auth_client.delete(f"/api/plants/{uuid.uuid4()}")
    assert response.status_code == 404


async def test_plant_delete_wrong_user(auth_client: AsyncClient):
    """Tests deleting plant by user that is not creator."""
    _, _, plant = await create_test_plant_instances()
    response = await auth_client.delete(f"/api/plants/{plant.uuid}")

    assert response.status_code == 403
    assert await Plant.all().count() == 1
    assert response.json().get("detail") == "You are not allowed to perform this action"


async def test_plant_delete_wrong_superuser(auth_client: AsyncClient):
    """Tests deleting plant by user that is not creator, but it's a superuser."""
    await User.filter(email="pytest@auth.com").update(is_superuser=True)
    _, _, plant = await create_test_plant_instances()
    response = await auth_client.delete(f"/api/plants/{plant.uuid}")

    assert response.status_code == 200
    assert await Plant.all().count() == 0
