import uuid
from unittest.mock import patch, MagicMock

from app.storage import s3_client, chunk_object_key, put_chunk

def test_chunk_object_key():
    session_id = uuid.uuid4()
    chunk_index = 5
    expected_key = f"sessions/{session_id}/chunks/0005.bin"
    assert chunk_object_key(session_id, chunk_index) == expected_key


@patch("app.storage.boto3.client")
def test_s3_client_secure(mock_boto_client, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "minio_secure", True)
    monkeypatch.setattr(settings, "minio_endpoint", "test-endpoint")
    monkeypatch.setattr(settings, "minio_access_key", "test-access-key")
    monkeypatch.setattr(settings, "minio_secret_key", "test-secret-key")

    s3_client.cache_clear()
    s3_client()

    mock_boto_client.assert_called_once()
    kwargs = mock_boto_client.call_args.kwargs
    assert kwargs["endpoint_url"] == "https://test-endpoint"
    assert kwargs["aws_access_key_id"] == "test-access-key"
    assert kwargs["aws_secret_access_key"] == "test-secret-key"
    assert kwargs["region_name"] == "us-east-1"
    assert mock_boto_client.call_args.kwargs["config"].signature_version == "s3v4"


@patch("app.storage.boto3.client")
def test_s3_client_insecure(mock_boto_client, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "minio_secure", False)
    monkeypatch.setattr(settings, "minio_endpoint", "test-endpoint")
    monkeypatch.setattr(settings, "minio_access_key", "test-access-key")
    monkeypatch.setattr(settings, "minio_secret_key", "test-secret-key")

    s3_client.cache_clear()
    s3_client()

    mock_boto_client.assert_called_once()
    kwargs = mock_boto_client.call_args.kwargs
    assert kwargs["endpoint_url"] == "http://test-endpoint"
    assert kwargs["aws_access_key_id"] == "test-access-key"
    assert kwargs["aws_secret_access_key"] == "test-secret-key"
    assert kwargs["region_name"] == "us-east-1"
    assert mock_boto_client.call_args.kwargs["config"].signature_version == "s3v4"


@patch("app.storage.s3_client")
def test_put_chunk_default_content_type(mock_s3_client, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "minio_bucket", "test-bucket")

    mock_client_instance = MagicMock()
    mock_s3_client.return_value = mock_client_instance

    session_id = uuid.uuid4()
    chunk_index = 0
    body = b"test body"
    expected_key = f"sessions/{session_id}/chunks/0000.bin"

    result_key = put_chunk(session_id, chunk_index, body, None)

    assert result_key == expected_key
    mock_s3_client.assert_called_once()
    mock_client_instance.put_object.assert_called_once_with(
        Bucket="test-bucket",
        Key=expected_key,
        Body=body,
        ContentType="application/octet-stream",
    )


@patch("app.storage.s3_client")
def test_put_chunk_custom_content_type(mock_s3_client, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "minio_bucket", "test-bucket")

    mock_client_instance = MagicMock()
    mock_s3_client.return_value = mock_client_instance

    session_id = uuid.uuid4()
    chunk_index = 1
    body = b"test body"
    custom_content_type = "audio/webm"
    expected_key = f"sessions/{session_id}/chunks/0001.bin"

    result_key = put_chunk(session_id, chunk_index, body, custom_content_type)

    assert result_key == expected_key
    mock_s3_client.assert_called_once()
    mock_client_instance.put_object.assert_called_once_with(
        Bucket="test-bucket",
        Key=expected_key,
        Body=body,
        ContentType=custom_content_type,
    )
