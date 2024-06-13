import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    TURSO_DATABASE_URL: str
    TURSO_AUTH_TOKEN: str
    PYALEX_EMAIL: str
    TEMPLATES_DIR: str = os.path.join(os.getcwd(), "templates")
    AUTH_USERNAME: str
    AUTH_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
