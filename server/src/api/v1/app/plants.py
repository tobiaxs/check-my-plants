from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

from src.database.models import Plant

router = APIRouter(tags=["Plants"], include_in_schema=False)

templates = Jinja2Templates("templates")


@router.get("/", status_code=200, response_class=HTMLResponse)
async def plants_dashboard(request: Request) -> templates.TemplateResponse:
    """Displays a list of all plants."""
    plants = await Plant.filter(is_accepted=False)
    context = {"request": request, "plants": plants}
    return templates.TemplateResponse("plants/dashboard.html", context)


@router.get("/plants/{pk}", status_code=200, response_class=HTMLResponse)
async def plant_details(pk: UUID, request: Request) -> templates.TemplateResponse:
    """Displays a details of given plant."""
    plant = await Plant.get_or_none(pk=pk)
    # TODO: Custom 404 page
    if not plant:
        raise HTTPException(status_code=404, detail="Plant does not exist")
    await plant.fetch_related("creator")
    context = {"request": request, "plant": plant}
    return templates.TemplateResponse("plants/details.html", context)


@router.get("/plant/create", status_code=200, response_class=HTMLResponse)
async def plant_create_form(request: Request) -> templates.TemplateResponse:
    """Displays a plant create from."""
    context = {"request": request}
    return templates.TemplateResponse("shared/403-page.html", context)
