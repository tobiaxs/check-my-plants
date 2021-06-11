from typing import Optional

from fastapi import Form
from pydantic import EmailStr, SecretStr

from src.api.forms.generic import GenericForm, ModelCreateForm
from src.database.models import User
from src.services.hashing import HashingService


class UserCreateForm(ModelCreateForm):
    """Form for registering users."""

    model = User

    def __init__(
        self,
        email: EmailStr = Form(...),
        password: SecretStr = Form(..., min_length=8, max_length=127),
        password_confirm: SecretStr = Form(...),
    ):
        """Builds the data based on form dependencies."""
        super().__init__()
        self.data = {
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
        }

    def clean(self):
        """Makes data ready to create an user instance."""
        email = self.data["email"]
        password = self.data["password"]
        self.data = {
            "email": email,
            "hashed_password": HashingService.get_hashed_password(password),
        }

    async def validate(self) -> None:
        """Checks if email is not in use and if the passwords match."""
        if await User.get_or_none(email=self.data["email"]):
            self.errors.append("User with that email already exists")
        if (
            not self.data["password"].get_secret_value()
            == self.data["password_confirm"].get_secret_value()
        ):
            self.errors.append("Passwords didn't match")


class UserLoginForm(GenericForm):
    """Form for authorizing users."""

    def __init__(
        self,
        email: EmailStr = Form(...),
        password: SecretStr = Form(...),
    ):
        """Builds the data based on form dependencies."""
        super().__init__()
        self.data = {"email": email, "password": password}
        self.user: Optional[User] = None

    async def validate(self) -> None:
        """Checks if user with given email exists
        and if password matches the one in the database.

        Additionally, assigns the user instance, to have it accessible later on.
        """
        self.user = await User.get_or_none(email=self.data["email"])
        if not self.user:
            return self.errors.append("User with that email does not exist")
        if not HashingService.verify_password(
            self.data["password"], self.user.hashed_password
        ):
            self.errors.append("Wrong email or password")
