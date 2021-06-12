from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")


def TemplateResponse(*args, **kwargs) -> templates.TemplateResponse:
    """Helper response which clears the cookies
    if user is not present in the context.
    """
    response = templates.TemplateResponse(*args, **kwargs)
    if not response.context.get("user"):
        response.delete_cookie("access_token")
    return response
