import time
import boto3
from botocore.client import Config
from app.config import settings

def test_s3_client_creation(iterations=100):
    start = time.time()
    for _ in range(iterations):
        scheme = "https" if settings.minio_secure else "http"
        client = boto3.client(
            "s3",
            endpoint_url=f"{scheme}://{settings.minio_endpoint}",
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )
    return time.time() - start

def test_s3_client_reuse(iterations=100):
    scheme = "https" if settings.minio_secure else "http"
    client = boto3.client(
        "s3",
        endpoint_url=f"{scheme}://{settings.minio_endpoint}",
        aws_access_key_id=settings.minio_access_key,
        aws_secret_access_key=settings.minio_secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )
    start = time.time()
    for _ in range(iterations):
        c = client
    return time.time() - start

if __name__ == "__main__":
    create_time = test_s3_client_creation()
    reuse_time = test_s3_client_reuse()
    print(f"Time to create client 100 times: {create_time:.4f}s")
    print(f"Time to reuse client 100 times: {reuse_time:.4f}s")
    print(f"Improvement: {create_time / reuse_time:.2f}x")
