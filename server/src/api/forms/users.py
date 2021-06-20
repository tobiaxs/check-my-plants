from fastapi import Depends, Form
from pydantic import SecretStr

from src.api.forms.generic import GenericForm, ModelCreateForm, ModelUpdateForm
from src.api.forms.validators.users import (
    EmailLengthValidator,
    OldPasswordCorrectValidator,
    PasswordCorrectValidator,
    PasswordLengthValidator,
    PasswordsMatchValidator,
    UserDontExistValidator,
    UserExistsValidator,
)
from src.api.middleware.context import context_middleware
from src.database.models import User
from src.services.hashing import HashingService


class UserCreateForm(ModelCreateForm):
    """Form for registering users."""

    model = User

    def __init__(
        self,
        email: str = Form(...),
        password: SecretStr = Form(...),
        password_confirm: SecretStr = Form(...),
    ):
        """Builds the data based on form dependencies."""
        super().__init__()
        self.data = {
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
        }
        self.validators = [
            EmailLengthValidator,
            UserExistsValidator,
            PasswordLengthValidator,
            PasswordsMatchValidator,
        ]

    async def clean(self):
        """Makes data ready to create an user instance."""
        email = self.data["email"]
        password = self.data["password"]
        self.data = {
            "email": email,
            "hashed_password": HashingService.get_hashed_password(password),
        }


class UserLoginForm(GenericForm):
    """Form for authorizing users."""

    def __init__(
        self,
        email: str = Form(...),
        password: SecretStr = Form(...),
    ):
        """Builds the data based on form dependencies."""
        super().__init__()
        self.data = {"email": email, "password": password}
        self.validators = [UserDontExistValidator, PasswordCorrectValidator]


class PasswordChangeForm(ModelUpdateForm):
    """Form for changing user password.

    Additionally, stores the context.
    """

    def __init__(
        self,
        context: dict = Depends(context_middleware),
        old_password: SecretStr = Form(...),
        password: SecretStr = Form(...),
        password_confirm: SecretStr = Form(...),
    ):
        """Builds the data based on form dependencies."""
        super().__init__()
        self.data = {
            "old_password": old_password,
            "password": password,
            "password_confirm": password_confirm,
            "email": getattr(context.get("user"), "email", None),
        }
        self.validators = [
            PasswordLengthValidator,
            PasswordsMatchValidator,
            OldPasswordCorrectValidator,
        ]
        self.context = context

    async def clean(self) -> None:
        """Sets the hashed password value."""
        self.data = {
            "hashed_password": HashingService.get_hashed_password(self.data["password"])
        }
