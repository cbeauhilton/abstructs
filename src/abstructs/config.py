from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    TURSO_DATABASE_URL: str
    TURSO_AUTH_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()
