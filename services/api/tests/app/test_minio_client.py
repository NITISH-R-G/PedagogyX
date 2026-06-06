import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from app.minio_client import ensure_bucket, _endpoint_url
from app.config import settings

def test_endpoint_url():
    with patch("app.minio_client.settings.minio_secure", True):
        with patch("app.minio_client.settings.minio_endpoint", "secure-host:9000"):
            assert _endpoint_url() == "https://secure-host:9000"

    with patch("app.minio_client.settings.minio_secure", False):
        with patch("app.minio_client.settings.minio_endpoint", "insecure-host:9000"):
            assert _endpoint_url() == "http://insecure-host:9000"

@patch("app.minio_client.boto3.client")
def test_ensure_bucket_exists(mock_boto3_client):
    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client

    ensure_bucket()

    mock_client.head_bucket.assert_called_once_with(Bucket=settings.minio_bucket)
    mock_client.create_bucket.assert_not_called()

@patch("app.minio_client.boto3.client")
def test_ensure_bucket_not_exists(mock_boto3_client):
    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client

    error_response = {"Error": {"Code": "404"}}
    mock_client.head_bucket.side_effect = ClientError(error_response, "HeadBucket")

    ensure_bucket()

    mock_client.head_bucket.assert_called_once_with(Bucket=settings.minio_bucket)
    mock_client.create_bucket.assert_called_once_with(Bucket=settings.minio_bucket)

@patch("app.minio_client.boto3.client")
def test_ensure_bucket_other_error(mock_boto3_client):
    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client

    error_response = {"Error": {"Code": "403"}}
    mock_client.head_bucket.side_effect = ClientError(error_response, "HeadBucket")

    with pytest.raises(ClientError):
        ensure_bucket()

    mock_client.head_bucket.assert_called_once_with(Bucket=settings.minio_bucket)
    mock_client.create_bucket.assert_not_called()
