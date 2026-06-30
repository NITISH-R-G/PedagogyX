import pytest
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from app.auth import verify_api_key
from app.config import settings

def test_verify_api_key_success(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "test_api_key")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="test_api_key")
    result = verify_api_key(credentials)
    assert result == "test_api_key"

def test_verify_api_key_invalid_scheme(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "test_api_key")
    credentials = HTTPAuthorizationCredentials(scheme="Basic", credentials="test_api_key")
    with pytest.raises(HTTPException) as exc_info:
        verify_api_key(credentials)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Invalid authentication scheme."

def test_verify_api_key_invalid_credentials(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "test_api_key")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_api_key")
    with pytest.raises(HTTPException) as exc_info:
        verify_api_key(credentials)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Invalid API Key"
