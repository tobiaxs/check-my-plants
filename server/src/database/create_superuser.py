from tortoise import run_async

from src.database.config import create_superuser

if __name__ == "__main__":
    run_async(create_superuser())
