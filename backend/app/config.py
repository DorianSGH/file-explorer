"""
Application configuration.

All environment variables are declared here. Importing `settings`
anywhere in the app gives a single, type-checked source of truth.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql://fileexplorer:fileexplorer@db:5432/fileexplorer"
    )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
