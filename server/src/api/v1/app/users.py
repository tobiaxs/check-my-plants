from fastapi import APIRouter, Form
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr, SecretStr
from starlette.requests import Request
from starlette.responses import HTMLResponse

from src.api.forms.users import UserCreateForm

router = APIRouter(tags=["Users"], include_in_schema=False)

templates = Jinja2Templates("templates")


@router.get("/register", status_code=200, response_class=HTMLResponse)
async def user_register_form(request: Request) -> templates.TemplateResponse:
    """Displays a user register form."""
    # TODO: Redirect to / if user exists
    context = {"request": request}
    return templates.TemplateResponse("users/register.html", context)


@router.get("/login", status_code=200, response_class=HTMLResponse)
async def user_login_form(request: Request) -> templates.TemplateResponse:
    """Displays a user login form."""
    # TODO: Redirect to / if user exists
    context = {"request": request}
    return templates.TemplateResponse("users/login.html", context)


@router.post("/register", status_code=200, response_class=HTMLResponse)
async def user_register(
    request: Request,
    email: EmailStr = Form(...),
    password: SecretStr = Form(..., min_length=8, max_length=127),
    password_confirm: SecretStr = Form(...),
) -> templates.TemplateResponse:
    """Registers a user using form data."""
    form = UserCreateForm(
        {
            "email": email,
            "password": password.get_secret_value(),
            "password_confirm": password_confirm.get_secret_value(),
        }
    )
    await form.validate()
    if form.errors:
        context = {"request": request, "errors": form.errors}
        return templates.TemplateResponse("users/register.html", context)
    else:
        await form.create()
        context = {"request": request, "messages": ["You can now login into our app"]}
        return templates.TemplateResponse("users/login.html", context)
