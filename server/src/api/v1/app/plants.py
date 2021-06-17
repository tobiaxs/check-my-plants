from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse, RedirectResponse

from src.api.forms.plants import PlantCreateForm
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
