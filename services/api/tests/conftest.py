import os
import pytest

@pytest.fixture(autouse=True)
def set_env_vars():
    os.environ["API_KEY"] = "dev_api_key_placeholder"
