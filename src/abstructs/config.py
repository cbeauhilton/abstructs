import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    TURSO_DATABASE_URL: str
    TURSO_AUTH_TOKEN: str
    PYALEX_EMAIL: str
    AUTH_USERNAME: str
    AUTH_PASSWORD: str
    TEMPLATES_DIR: str = str(Path(__file__).resolve().parent.parent / "templates")

    class Config:
        env_file = ".env"


settings = Settings()
