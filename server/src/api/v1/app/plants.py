from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse, RedirectResponse

from src.api.forms.plants import PlantCreateForm, PlantEditForm
from src.api.middleware.context import context_middleware
from src.api.middleware.response import TemplateResponse
from src.database.models import Plant

router = APIRouter(tags=["Plants"], include_in_schema=False)


@router.get("/", status_code=200, response_class=HTMLResponse)
async def plants_dashboard(context: dict = Depends(context_middleware)) -> HTMLResponse:
    """Displays a list of all plants."""
    plants = await Plant.filter(is_accepted=False).prefetch_related(
        "image"
    )  # TODO: Change to True
    context["plants"] = plants
    return TemplateResponse("plants/dashboard.html", context)


@router.get("/plants/{pk}", status_code=200, response_class=HTMLResponse)
async def plant_details(
    pk: UUID, context: dict = Depends(context_middleware)
) -> HTMLResponse:
    """Displays a details of given plant if it exists."""
    plant = await Plant.get_or_none(pk=pk)
    if not plant:
        return TemplateResponse("shared/404-page.html", context, 404)
    await plant.fetch_related("creator", "image")
    context["plant"] = plant
    return TemplateResponse("plants/details.html", context)


@router.get("/plant/create", status_code=200, response_class=HTMLResponse)
async def plant_create_form(
    context: dict = Depends(context_middleware),
) -> HTMLResponse:
    """Displays a plant create from."""
    if not context.get("user"):
        return TemplateResponse("shared/403-page.html", context, 403)
    return TemplateResponse("plants/create.html", context)


@router.post("/plant/create", status_code=201, response_class=HTMLResponse)
async def plant_create(
    form: PlantCreateForm = Depends(),
) -> Union[HTMLResponse, RedirectResponse]:
    """Creates a plant instance based on form data."""
    context = form.context.copy()
    if not form.context.get("user"):
        return TemplateResponse("shared/403-page.html", context, 403)
    await form.validate()
    if form.errors:
        context["errors"] = form.errors
        return TemplateResponse("plants/create.html", context, 422)
    plant = await form.create()
    return RedirectResponse(f"/plants/{plant.uuid}", 302)


@router.post("/plant/delete/{pk}", status_code=200, response_class=HTMLResponse)
async def plant_delete(
    pk: UUID, context: dict = Depends(context_middleware)
) -> HTMLResponse:
    """Deletes the plant if it exists and given user is its creator."""
    plant = await Plant.get_or_none(pk=pk)
    if not plant:
        return TemplateResponse("shared/404-page.html", context, 404)
    user = context.get("user")
    await plant.fetch_related("creator")
    if not user or not user == plant.creator:
        return TemplateResponse("shared/403-page.html", context, 403)
    await plant.delete()
    context["messages"] = ["Plant has been deleted successfully"]
    return TemplateResponse("plants/create.html", context, 200)


@router.get("/plant/edit/{pk}", status_code=200, response_class=HTMLResponse)
async def plant_edit_form(
    pk: UUID, context: dict = Depends(context_middleware)
) -> HTMLResponse:
    """Displays the plant edit form for given plant if correct user is present."""
    # TODO: Some `ViewHelper` class should deal with those initial `if` statements
    plant = await Plant.get_or_none(pk=pk)
    if not plant:
        return TemplateResponse("shared/404-page.html", context, 404)
    user = context.get("user")
    await plant.fetch_related("creator")
    if not user or not user == plant.creator:
        return TemplateResponse("shared/403-page.html", context, 403)
    await plant.fetch_related("creator")
    await plant.fetch_related("image")
    context["plant"] = plant
    return TemplateResponse("plants/edit.html", context, 200)


@router.post("/plant/edit/{pk}", status_code=200, response_class=HTMLResponse)
async def plant_edit(
    pk: UUID,
    form: PlantEditForm = Depends(),
) -> HTMLResponse:
    """Edits given plant with given form data."""
    # TODO: Again, `ViewHelper` dependency...
    context = form.context
    plant = await Plant.get_or_none(pk=pk)
    if not plant:
        return TemplateResponse("shared/404-page.html", context, 404)
    user = context.get("user")
    await plant.fetch_related("creator")
    if not user or not user == plant.creator:
        return TemplateResponse("shared/403-page.html", context, 403)
    await form.validate()
    context["plant"] = plant
    if form.errors:
        context["errors"] = form.errors
        return TemplateResponse("plants/edit.html", context, 422)
    await form.update(plant)
    context["messages"] = ["Plant has been edited successfully!"]
    return TemplateResponse("plants/edit.html", context, 200)
