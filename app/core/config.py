# app/core/config.py
# pylint: disable=too-few-public-methods
import os

from dotenv import load_dotenv

# Cargar el archivo .env solo una vez
load_dotenv()


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL must be set in the environment variables.")
    return f"{database_url.split('://')[0]}+asyncpg://{database_url.split('://')[1]}"


class Settings:
    DATABASE_URL = get_database_url()
    DATABASE_URL_TRIG = os.getenv("DATABASE_URL")


# Crear una instancia de Settings
settings = Settings()