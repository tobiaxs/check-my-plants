import shutil

from tortoise import fields

from src.database.models.generic import GenericModel


class Image(GenericModel):
    """Model containing info about the image file."""

    name = fields.CharField(max_length=127)
    path = fields.CharField(max_length=255)

    async def delete(self, *args, **kwargs) -> None:
        """Deletes the image instance and connected image file."""
        if shutil.which(self.path):
            shutil.rmtree(self.path)
        await super().delete(*args, **kwargs)
