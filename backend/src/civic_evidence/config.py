# Application configuration loaded from the environment.
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_SQLITE_DB = _REPO_ROOT / "data" / "civic_evidence.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    secret_key: str = "dev-secret-key-change-me-please-123456"
    jwt_algorithm: str = "HS256"
    jwt_default_ttl_minutes: int = 60
    auth_required: bool = False
    allow_demo_auth: bool = True
    demo_user_id: str = "local-dev-user"
    demo_roles: list[str] = ["reviewer", "admin"]
    cors_origins: list[str] = ["http://localhost:3000"]
    log_level: str = "INFO"

    database_url: str = f"sqlite:///{_DEFAULT_SQLITE_DB}"

    audio_storage_backend: str = "local"
    audio_storage_dir: str = "./data/raw/audio"
    document_storage_dir: str = "./data/processed/documents"
    max_upload_mb: int = 200

    n_atlas_base_url: str = ""
    n_atlas_api_key: str = ""
    n_atlas_model_id: str = ""
    n_atlas_timeout_seconds: int = 60

    civic_index_dir: str = "./data/processed/civic_index"

    @model_validator(mode="after")
    def validate_runtime_settings(self) -> "Settings":
        env = self.app_env.lower()
        if env == "production":
            default_secret = "dev-secret-key-change-me-please-123456"
            if self.secret_key in {"", default_secret} or len(self.secret_key) < 32:
                raise ValueError("A production deployment requires a strong secret_key (32+ chars) in the environment.")
            if self.allow_demo_auth:
                raise ValueError("Demo authentication must be disabled in production.")
            if self.database_url.startswith("sqlite://"):
                raise ValueError("Production requires a non-SQLite database_url (for example PostgreSQL).")
            if not self.cors_origins or any(origin.strip() in {"", "*"} for origin in self.cors_origins):
                raise ValueError("Production requires explicit, non-wildcard CORS origins.")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
