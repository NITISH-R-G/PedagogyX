import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError

from app.minio_client import ensure_bucket
from app.config import settings


@patch("app.minio_client.boto3.client")
def test_ensure_bucket_exists(mock_boto3_client):
    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client

    # head_bucket succeeds without raising exception
    mock_client.head_bucket.return_value = {}

    ensure_bucket()

    mock_client.head_bucket.assert_called_once_with(Bucket=settings.minio_bucket)
    mock_client.create_bucket.assert_not_called()


@pytest.mark.parametrize("error_code", ["404", "NoSuchBucket", "NotFound"])
@patch("app.minio_client.boto3.client")
def test_ensure_bucket_not_found_handled(mock_boto3_client, error_code):
    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client

    # head_bucket raises ClientError with specific Code
    error_response = {"Error": {"Code": error_code, "Message": "Not Found"}}
    mock_client.head_bucket.side_effect = ClientError(error_response, "HeadBucket")

    ensure_bucket()

    mock_client.head_bucket.assert_called_once_with(Bucket=settings.minio_bucket)
    mock_client.create_bucket.assert_called_once_with(Bucket=settings.minio_bucket)


@patch("app.minio_client.boto3.client")
def test_ensure_bucket_other_error(mock_boto3_client):
    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client

    # head_bucket raises ClientError with different Code
    error_response = {"Error": {"Code": "500", "Message": "Internal Error"}}
    mock_client.head_bucket.side_effect = ClientError(error_response, "HeadBucket")

    with pytest.raises(ClientError):
        ensure_bucket()

    mock_client.head_bucket.assert_called_once_with(Bucket=settings.minio_bucket)
    mock_client.create_bucket.assert_not_called()
