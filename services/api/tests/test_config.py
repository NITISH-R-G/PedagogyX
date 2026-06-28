import pytest
from app.config import Settings


@pytest.fixture
def clean_env(monkeypatch):
    # Remove any existing env vars that might interfere with defaults
    env_vars = [
        "DATABASE_URL",
        "REDIS_URL",
        "MINIO_ENDPOINT",
        "MINIO_ACCESS_KEY",
        "MINIO_SECRET_KEY",
        "MINIO_BUCKET",
        "MINIO_SECURE",
        "JOB_QUEUE_ASR",
        "JOB_QUEUE_METRICS",
        "OVERVIEW_ROOMS_TARGET",
        "MAX_UPLOAD_BYTES",
        "API_KEY",
    ]
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)


def test_settings_default(clean_env):
    settings = Settings(_env_file=None)

    assert settings.database_url is None
    assert settings.redis_url == "redis://localhost:6379"
    assert settings.minio_endpoint == "localhost:9000"
    assert settings.minio_access_key is None
    assert settings.minio_secret_key is None
    assert settings.minio_bucket == "pedagogyx-uploads"
    assert settings.minio_secure is True
    assert settings.job_queue_asr == "jobs:asr"
    assert settings.job_queue_metrics == "jobs:talk_ratio"
    assert settings.overview_rooms_target == 20
    assert settings.max_upload_bytes == 52_428_800
    assert settings.api_key is None


def test_settings_overrides(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("MINIO_ENDPOINT", "minio:9000")
    monkeypatch.setenv("MINIO_ACCESS_KEY", "access")
    monkeypatch.setenv("MINIO_SECRET_KEY", "secret")
    monkeypatch.setenv("MINIO_BUCKET", "test-bucket")
    monkeypatch.setenv("MINIO_SECURE", "True")
    monkeypatch.setenv("JOB_QUEUE_ASR", "test-asr")
    monkeypatch.setenv("JOB_QUEUE_METRICS", "test-metrics")
    monkeypatch.setenv("OVERVIEW_ROOMS_TARGET", "50")
    monkeypatch.setenv("MAX_UPLOAD_BYTES", "1024")
    monkeypatch.setenv("API_KEY", "test-api-key")

    settings = Settings(_env_file=None)

    assert settings.database_url == "postgresql://user:pass@localhost:5432/db"
    assert settings.redis_url == "redis://localhost:6379/0"
    assert settings.minio_endpoint == "minio:9000"
    assert settings.minio_access_key == "access"
    assert settings.minio_secret_key == "secret"
    assert settings.minio_bucket == "test-bucket"
    assert settings.minio_secure is True
    assert settings.job_queue_asr == "test-asr"
    assert settings.job_queue_metrics == "test-metrics"
    assert settings.overview_rooms_target == 50
    assert settings.max_upload_bytes == 1024
    assert settings.api_key == "test-api-key"
