# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app import app  # Adjust this import if your main app file is named differently

@pytest.fixture(scope="module")
def client():
    """Fixture to provide a FastAPI test client."""
    return TestClient(app)
