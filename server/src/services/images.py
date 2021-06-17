import shutil
import uuid

from fastapi import UploadFile

from src.database.models import Image


class ImageService:
    """Helper class for actions related with image files."""

    @classmethod
    async def create_image(cls, image_file: UploadFile, folder: str) -> Image:
        """Creates a file and creates an image model instance."""
        file_location = cls.generate_image_path(image_file.filename, folder)
        cls.create_file(file_location, image_file)
        image = await Image.create(name=image_file.filename, path=file_location[1:])
        return image

    @staticmethod
    def create_file(file_location: str, image_file: UploadFile) -> None:
        """Adds an image file based on the uploaded image to the static folder."""
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(image_file.file, file_object)

    @staticmethod
    def generate_image_path(file_name: str, folder: str) -> str:
        """Creates a full image file path based on file extension,
        folder name and random uuid.
        """
        extension = file_name.split(".")[-1]
        prefix = f"./static/{folder}"
        file_uuid = uuid.uuid4()
        image_path = f"{prefix}/{file_uuid}.{extension}"
        return image_path
