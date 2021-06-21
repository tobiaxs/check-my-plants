from datetime import datetime, timezone
from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from src.api.forms.users import PasswordChangeForm, UserCreateForm, UserLoginForm
from src.api.middleware.context import context_middleware
from src.api.middleware.response import TemplateResponse
from src.database.models import Plant, User
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
        return TemplateResponse("users/login.html", context, 422)
    token = JwtTokenService.encode_jwt(form.data["email"])
    response = RedirectResponse("/", 302)
    response.set_cookie("access_token", f"Bearer {token.access_token}")
    return response


@router.get("/logout", status_code=200, response_class=RedirectResponse)
async def user_logout(request: Request) -> RedirectResponse:
    """Clears the cookies and redirects to the dashboard."""
    context = {
        "request": request,
        "messages": ["You have been logged out successfully"],
    }
    response = TemplateResponse("users/login.html", context)
    response.delete_cookie("access_token")
    return response


@router.get("/profile/{pk}", status_code=200, response_class=HTMLResponse)
async def user_profile(
    pk: UUID, context: dict = Depends(context_middleware)
) -> HTMLResponse:
    """Prepares the context and displays a user profile page."""
    profile_user = await User.get_or_none(pk=pk)
    if not profile_user:
        return TemplateResponse("shared/404-page.html", context, 404)
    plants = await Plant.filter(creator=profile_user).prefetch_related("image")
    context["days_since_join"] = (
        datetime.now(timezone.utc) - profile_user.created_at
    ).days
    context["profile_user"] = profile_user
    context["plants"] = plants
    return TemplateResponse("users/profile.html", context)


@router.post("/profile/{pk}", status_code=200, response_class=HTMLResponse)
async def user_delete(
    pk: UUID, context: dict = Depends(context_middleware)
) -> HTMLResponse:
    """Deletes the user if it matches the one in the context
    and redirects to the dashboard page.
    """
    profile_user = await User.get_or_none(pk=pk)
    if not profile_user:
        return TemplateResponse("shared/404-page.html", context, 404)
    user = context.get("user")
    if not user or not user == profile_user:
        return TemplateResponse("shared/403-page.html", context, 403)
    await profile_user.delete()
    context.pop("user")
    context["messages"] = ["User has been deleted successfully."]
    return TemplateResponse("users/login.html", context, 200)


@router.get("/change_password/{pk}", status_code=200, response_class=HTMLResponse)
async def change_password_form(
    pk: UUID, context: dict = Depends(context_middleware)
) -> HTMLResponse:
    """Displays the password change form if correct user is logged in."""
    profile_user = await User.get_or_none(pk=pk)
    if not profile_user:
        return TemplateResponse("shared/404-page.html", context, 404)
    user = context.get("user")
    if not user or not user == profile_user:
        return TemplateResponse("shared/403-page.html", context, 403)
    return TemplateResponse("users/change_password.html", context, 200)


@router.post("/change_password/{pk}", status_code=200, response_class=HTMLResponse)
async def change_password(
    pk: UUID, form: PasswordChangeForm = Depends()
) -> HTMLResponse:
    """Changes user password using password change form
    and redirects back to the form.
    """
    context = form.context
    profile_user = await User.get_or_none(pk=pk)
    if not profile_user:
        return TemplateResponse("shared/404-page.html", context, 404)
    user = context.get("user")
    if not user or not user == profile_user:
        return TemplateResponse("shared/403-page.html", context, 403)
    await form.validate()
    if form.errors:
        context["errors"] = form.errors
        return TemplateResponse("users/change_password.html", context, 422)
    await form.update(profile_user)
    context["messages"] = ["Password has been changed successfully!"]
    return TemplateResponse("users/change_password.html", context, 200)
