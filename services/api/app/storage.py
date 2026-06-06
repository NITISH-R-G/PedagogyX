from uuid import UUID

import boto3
from botocore.client import Config

from app.config import settings


_s3_client = None

def s3_client():
    global _s3_client
    if _s3_client is None:
        scheme = "https" if settings.minio_secure else "http"
        _s3_client = boto3.client(
            "s3",
            endpoint_url=f"{scheme}://{settings.minio_endpoint}",
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )
    return _s3_client


def chunk_object_key(session_id: UUID, chunk_index: int) -> str:
    return f"sessions/{session_id}/chunks/{chunk_index:04d}.bin"


def put_chunk(session_id: UUID, chunk_index: int, body: bytes, content_type: str | None) -> str:
    key = chunk_object_key(session_id, chunk_index)
    client = s3_client()
    client.put_object(
        Bucket=settings.minio_bucket,
        Key=key,
        Body=body,
        ContentType=content_type or "application/octet-stream",
    )
    return key
