import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.config import settings


def ensure_bucket() -> None:
    client = boto3.client(
        "s3",
        endpoint_url=_endpoint_url(),
        aws_access_key_id=settings.minio_access_key,
        aws_secret_access_key=settings.minio_secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )
    try:
        client.head_bucket(Bucket=settings.minio_bucket)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchBucket", "NotFound"):
            client.create_bucket(Bucket=settings.minio_bucket)
        else:
            raise


def _endpoint_url() -> str:
    scheme = "https" if settings.minio_secure else "http"
    return f"{scheme}://{settings.minio_endpoint}"
