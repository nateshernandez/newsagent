from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed settings loaded from environment variables (and optional .env file)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "local"
    bedrock_agentcore_memory_id: str | None = None
    aws_region: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the application settings (singleton; env is read once)."""
    return Settings()
