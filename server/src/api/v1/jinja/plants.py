from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

router = APIRouter(tags=["Plants"], include_in_schema=False)

templates = Jinja2Templates("templates")


@router.get("/", status_code=200)
def plants_dashboard(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("plants/dashboard.html", {"request": request})
