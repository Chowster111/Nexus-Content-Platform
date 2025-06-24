# tests/integration/conftest.py
import pytest
from httpx import AsyncClient
from app import app  # Adjust import based on your actual FastAPI app location

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
