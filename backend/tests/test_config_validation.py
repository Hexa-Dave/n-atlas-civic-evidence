import pytest

from civic_evidence.config import Settings


def test_local_development_settings_allow_demo_auth():
    settings = Settings(app_env="development", allow_demo_auth=True, database_url="sqlite:///tmp/test.db")
    assert settings.app_env == "development"
    assert settings.allow_demo_auth is True


def test_production_requires_strong_secret_and_no_demo_auth():
    with pytest.raises(ValueError, match="strong secret_key"):
        Settings(
            app_env="production",
            secret_key="dev-secret-key-change-me-please-123456",
            allow_demo_auth=False,
            database_url="postgresql+psycopg://user:pass@localhost:5432/civic_evidence",
            cors_origins=["https://example.com"],
        )

    with pytest.raises(ValueError, match="Demo authentication"):
        Settings(
            app_env="production",
            secret_key="this-is-a-long-production-secret-12345",
            allow_demo_auth=True,
            database_url="postgresql+psycopg://user:pass@localhost:5432/civic_evidence",
            cors_origins=["https://example.com"],
        )

    with pytest.raises(ValueError, match="non-SQLite"):
        Settings(
            app_env="production",
            secret_key="this-is-a-long-production-secret-12345",
            allow_demo_auth=False,
            database_url="sqlite:////tmp/local.db",
            cors_origins=["https://example.com"],
        )
