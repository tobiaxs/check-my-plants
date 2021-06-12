from src.api.forms.validators.generic import GenericValidator
from src.database.models import User
from src.services.hashing import HashingService


class EmailLengthValidator(GenericValidator):
    def validate(self, data: dict) -> None:
        """Checks the email length."""
        email_len = len(data["email"])
        if email_len < 8:
            self.errors.append("Email address is too short")
        if email_len > 127:
            self.errors.append("Email address is too long")


class UserExistsValidator(GenericValidator):
    async def validate(self, data: dict) -> None:
        """Checks if user already exists."""
        if await User.get_or_none(email=data["email"]):
            self.errors.append("User with that email already exists")


class PasswordLengthValidator(GenericValidator):
    def validate(self, data: dict) -> None:
        """Checks the password length."""
        password_len = len(data["password"].get_secret_value())
        if password_len < 8:
            self.errors.append("Password is too short")
        if password_len > 123:
            self.errors.append("Password is too long")


class PasswordsMatchValidator(GenericValidator):
    def validate(self, data: dict) -> None:
        """Checks if passwords match."""
        if (
            not data["password"].get_secret_value()
                == data["password_confirm"].get_secret_value()
        ):
            self.errors.append("Passwords didn't match")


class UserDontExistValidator(GenericValidator):
    async def validate(self, data: dict) -> None:
        """Checks if user does not exist."""
        if not await User.get_or_none(email=data["email"]):
            return self.errors.append("User with that email does not exist")


class PasswordCorrectValidator(GenericValidator):
    async def validate(self, data: dict) -> None:
        """Checks if password is correct comparing to one stored in the db."""
        user = await User.get_or_none(email=data["email"])
        if not user:
            return
        if not HashingService.verify_password(
            data["password"], user.hashed_password
        ):
            self.errors.append("Wrong email or password")
