from passlib.context import CryptContext
from pydantic import SecretStr

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashingService:
    """Service for hashing & verifying passwords."""

    @staticmethod
    def get_hashed_password(password: SecretStr) -> str:
        """Passed plain string returns hashed password."""
        return password_context.hash(password.get_secret_value())

    @staticmethod
    def verify_password(plain_password: SecretStr, hashed_password: str) -> bool:
        """Checks if given plain string matched hashed password after getting hashed."""
        return password_context.verify(
            plain_password.get_secret_value(), hashed_password
        )
