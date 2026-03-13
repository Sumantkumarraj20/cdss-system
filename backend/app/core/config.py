"""Application configuration using pydantic settings.

This keeps runtime configuration centralized and allows overriding via env vars.
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CDSS Backend"
    debug: bool = False
    database_url: str = Field(
        "postgresql+psycopg2://cdss_user:strongpassword@localhost/cdss_db",
        env="DATABASE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_prefix="CDSS_",
    )


@lru_cache
def get_settings() -> "Settings":
    """Return a cached settings instance to avoid redundant parsing."""

    return Settings()


settings = get_settings()
