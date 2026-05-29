from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str | None = None
    redis_url: str | None = None
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str | None = None
    minio_secret_key: str | None = None
    minio_bucket: str = "pedagogyx-uploads"
    minio_secure: bool = False
    job_queue_asr: str = "jobs:asr"
    job_queue_metrics: str = "jobs:talk_ratio"
    overview_rooms_target: int = 20
    max_upload_bytes: int = 52_428_800  # 50 MiB
    api_key: str | None = None


settings = Settings()
