from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "AgentTrust-OS"
    app_env: str = "development"
    debug: bool = False

    database_url: str = Field(..., validation_alias="DATABASE_URL")
    redis_url: str = Field(..., validation_alias="REDIS_URL")

    jwt_secret: str = Field(..., validation_alias="JWT_SECRET")
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    jwt_refresh_token_expire_days: int = Field(
        default=30,
        validation_alias="JWT_REFRESH_TOKEN_EXPIRE_DAYS",
    )

    frontend_url: str = Field(
        default="http://localhost:5173",
        validation_alias="FRONTEND_URL",
    )

    ai_api_key: str | None = Field(
        default=None,
        validation_alias="AI_API_KEY",
    )
    ai_provider: str | None = Field(
        default=None,
        validation_alias="AI_PROVIDER",
    )
    ai_model: str | None = Field(
        default=None,
        validation_alias="AI_MODEL",
    )

    default_language: str = Field(
        default="en",
        validation_alias="DEFAULT_LANGUAGE",
    )
    supported_languages: str = Field(
        default="en,hi",
        validation_alias="SUPPORTED_LANGUAGES",
    )

    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("default_language")
    @classmethod
    def validate_default_language(cls, value: str) -> str:
        if value not in {"en", "hi"}:
            raise ValueError("DEFAULT_LANGUAGE must be 'en' or 'hi'")
        return value

    @field_validator("supported_languages")
    @classmethod
    def validate_supported_languages(cls, value: str) -> str:
        languages = {
            language.strip()
            for language in value.split(",")
            if language.strip()
        }

        if languages != {"en", "hi"}:
            raise ValueError(
                "SUPPORTED_LANGUAGES must contain exactly 'en' and 'hi'"
            )

        return "en,hi"


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()


settings = get_settings()