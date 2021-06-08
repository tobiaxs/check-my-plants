from src.api.forms.generic import ModelCreateForm
from src.database.models import User
from src.services.hashing import HashingService


class UserCreateForm(ModelCreateForm):
    """Form for registering user."""

    model = User

    def clean(self):
        """Makes data ready to create user instance."""
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
