# Application configuration loaded from the environment.
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    secret_key: str = "change-me"
    cors_origins: list[str] = ["http://localhost:3000"]
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://civic:civic@localhost:5432/civic_evidence"

    audio_storage_backend: str = "local"
    audio_storage_dir: str = "./data/raw/audio"
    document_storage_dir: str = "./data/processed/documents"
    max_upload_mb: int = 200

    n_atlas_base_url: str = ""
    n_atlas_api_key: str = ""
    n_atlas_model_id: str = ""
    n_atlas_timeout_seconds: int = 60

    civic_index_dir: str = "./data/processed/civic_index"


@lru_cache
def get_settings() -> Settings:
    return Settings()
