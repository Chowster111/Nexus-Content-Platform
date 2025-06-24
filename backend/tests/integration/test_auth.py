# tests/integration/test_auth.py
import pytest

@pytest.mark.asyncio
async def test_get_session_info(client):
    response = await client.get("/auth/session")
    assert response.status_code in (200, 401)
