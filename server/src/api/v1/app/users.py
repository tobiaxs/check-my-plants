from typing import Union

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from src.api.forms.users import UserCreateForm, UserLoginForm
from src.api.middleware.context import context_middleware
from src.api.middleware.response import TemplateResponse
from src.services.jwt_token import JwtTokenService

router = APIRouter(tags=["Users"], include_in_schema=False)


@router.get("/register", status_code=200, response_class=HTMLResponse)
async def user_register_form(
    context: dict = Depends(context_middleware),
) -> Union[HTMLResponse, RedirectResponse]:
    """Displays a user register form or redirects to dashboard
    if user is already logged in.
    """
    if context.get("user"):
        return RedirectResponse("/")
    return TemplateResponse("users/register.html", context)


@router.get("/login", status_code=200, response_class=HTMLResponse)
async def user_login_form(
    context: dict = Depends(context_middleware),
) -> Union[HTMLResponse, RedirectResponse]:
    """Displays a user login form or redirects to dashboard
    if user is already logged in.
    """
    if context.get("user"):
        return RedirectResponse("/")
    return TemplateResponse("users/login.html", context)


@router.post("/register", status_code=201, response_class=HTMLResponse)
async def user_register(
    request: Request, form: UserCreateForm = Depends()
) -> HTMLResponse:
    """Registers a user using form data and redirects to login form."""
    await form.validate()
    if form.errors:
        context = {"request": request, "errors": form.errors}
        return TemplateResponse("users/register.html", context, 422)
    await form.create()
    context = {"request": request, "messages": ["You can now login into our app"]}
    return TemplateResponse("users/login.html", context, 201)


@router.post("/login", status_code=200, response_class=HTMLResponse)
async def user_login(
    request: Request, form: UserLoginForm = Depends()
) -> Union[HTMLResponse, RedirectResponse]:
    """Logs user in, saves the cookies and redirects to the dashboard"""
    await form.validate()
    if form.errors:
        context = {"request": request, "errors": form.errors}
        return TemplateResponse("users/login.html", context)
    token = JwtTokenService.encode_jwt(form.data["email"])
    response = RedirectResponse("/", 302)
    response.set_cookie("access_token", f"Bearer {token.access_token}")
    return response


@router.get("/logout", status_code=200, response_class=RedirectResponse)
async def user_logout() -> RedirectResponse:
    """Clears the cookies and redirects to the dashboard."""
    response = RedirectResponse("/")
    response.delete_cookie("access_token")
    return response
