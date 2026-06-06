import os
from unittest import mock

from app.config import Settings


def test_settings_default_values():
    """Test that Settings initializes with expected default values when no env vars are set."""
    # We clear the environment to ensure no env vars interfere with the defaults
    with mock.patch.dict(os.environ, clear=True):
        settings = Settings()
        assert settings.database_url is None
        assert settings.redis_url is None
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


def test_settings_env_var_override():
    """Test that environment variables override the default values."""
    mock_env = {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/db",
        "REDIS_URL": "redis://localhost:6379/0",
        "MINIO_ENDPOINT": "s3.amazonaws.com",
        "MINIO_ACCESS_KEY": "test_access_key",
        "MINIO_SECRET_KEY": "test_secret_key",
        "MINIO_BUCKET": "test-bucket",
        "MINIO_SECURE": "true",
        "JOB_QUEUE_ASR": "test:queue:asr",
        "JOB_QUEUE_METRICS": "test:queue:metrics",
        "OVERVIEW_ROOMS_TARGET": "50",
        "MAX_UPLOAD_BYTES": "1000000",
        "API_KEY": "super_secret_api_key",
    }

    with mock.patch.dict(os.environ, mock_env, clear=True):
        settings = Settings()
        assert settings.database_url == "postgresql://user:pass@localhost:5432/db"
        assert settings.redis_url == "redis://localhost:6379/0"
        assert settings.minio_endpoint == "s3.amazonaws.com"
        assert settings.minio_access_key == "test_access_key"
        assert settings.minio_secret_key == "test_secret_key"
        assert settings.minio_bucket == "test-bucket"
        assert settings.minio_secure is True
        assert settings.job_queue_asr == "test:queue:asr"
        assert settings.job_queue_metrics == "test:queue:metrics"
        assert settings.overview_rooms_target == 50
        assert settings.max_upload_bytes == 1000000
        assert settings.api_key == "super_secret_api_key"


def test_settings_partial_env_var_override():
    """Test that only specified environment variables are overridden."""
    mock_env = {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/db",
        "MINIO_SECURE": "true",
    }

    with mock.patch.dict(os.environ, mock_env, clear=True):
        settings = Settings()
        assert settings.database_url == "postgresql://user:pass@localhost:5432/db"
        assert settings.minio_endpoint == "localhost:9000"  # Default
        assert settings.minio_secure is True
        assert settings.overview_rooms_target == 20  # Default
