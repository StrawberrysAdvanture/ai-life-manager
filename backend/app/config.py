from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Life Manager"
    environment: str = "development"

    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_life_manager"
    )
    test_database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_life_manager_test"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
