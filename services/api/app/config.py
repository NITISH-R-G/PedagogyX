import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/pedagogyx")
    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    minio_endpoint: str = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key: str = os.environ.get("MINIO_ACCESS_KEY", "")
    minio_secret_key: str = os.environ.get("MINIO_SECRET_KEY", "")
    minio_bucket: str = os.environ.get("MINIO_BUCKET", "pedagogyx-uploads")
    minio_secure: bool = os.environ.get("MINIO_SECURE", "False").lower() in ("true", "1", "t")
    job_queue_asr: str = "jobs:asr"
    job_queue_metrics: str = "jobs:talk_ratio"
    overview_rooms_target: int = 20
    max_upload_bytes: int = 52_428_800  # 50 MiB


settings = Settings()
