from fastapi import Form
from pydantic import SecretStr

from src.api.forms.generic import GenericForm, ModelCreateForm
from src.api.forms.validators.users import EmailLengthValidator, UserExistsValidator, PasswordLengthValidator, \
    PasswordsMatchValidator, UserDontExistValidator, PasswordCorrectValidator
from src.database.models import User
from src.services.hashing import HashingService


class UserCreateForm(ModelCreateForm):
    """Form for registering users."""

    model = User

    def __init__(
        self,
        email: str = Form(...),
        password: SecretStr = Form(...),
        password_confirm: SecretStr = Form(...)
    ):
        """Builds the data based on form dependencies."""
        super().__init__()
        self.data = {
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
        }
        self.validators = [EmailLengthValidator, UserExistsValidator, PasswordLengthValidator,
                           PasswordsMatchValidator]

    def clean(self):
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
