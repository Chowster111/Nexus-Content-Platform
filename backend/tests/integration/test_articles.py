# tests/integration/test_articles.py
import pytest

@pytest.mark.asyncio
async def test_get_all_articles(client):
    response = await client.get("/articles/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "data" in data or "results" in data  # depending on your route response
