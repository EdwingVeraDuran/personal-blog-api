from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.
    All values are loaded from environment variables (.env).
    """

    # ---------------------------------------------------------------------
    # App
    # ---------------------------------------------------------------------
    ENV: str = Field(default="dev")
    APP_NAME: str = Field(default="personal-blog-api")
    APP_PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)

    # ---------------------------------------------------------------------
    # Database
    # ---------------------------------------------------------------------
    DATABASE_URL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # ---------------------------------------------------------------------
    # Security / JWT
    # ---------------------------------------------------------------------
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    JWT_ACCESS_EXPIRES_MIN: int = 30
    JWT_REFRESH_EXPIRES_DAYS: int = 7

    # ---------------------------------------------------------------------
    # CORS
    # ---------------------------------------------------------------------
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # ---------------------------------------------------------------------
    # Admin
    # ---------------------------------------------------------------------
    ADMIN_EMAIL: str | None = None

    # ---------------------------------------------------------------------
    # Pydantic settings
    # ---------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def is_dev(self) -> bool:
        return self.ENV == "dev"

    @property
    def is_prod(self) -> bool:
        return self.ENV == "prod"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    Ensures env vars are read once.
    """
    return Settings()  # pyright: ignore[reportCallIssue]


# singleton importable
settings = get_settings()
