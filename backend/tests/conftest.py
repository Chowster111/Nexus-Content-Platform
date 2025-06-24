import pytest
from fastapi.testclient import TestClient
from app import app  # assuming your FastAPI app is in main.py

@pytest.fixture(scope="module")
def test_client():
    """
    Provides a TestClient instance for the entire test module.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def example_like_payload():
    """
    Returns a sample like payload dictionary.
    """
    return {
        "user_id": "test-user-123",
        "likes": [
            {"url": "https://example.com/article1", "liked": True},
            {"url": "https://example.com/article2", "liked": False}
        ]
    }
