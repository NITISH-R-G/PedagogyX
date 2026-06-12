import pytest
from app import db_utils

@pytest.fixture(autouse=True)
def reset_db_pool():
    """
    Ensure the global database pool state is reset before and after each test
    to prevent stale mocks from leaking across tests.
    """
    db_utils._db_pool = None
    yield
    db_utils._db_pool = None
