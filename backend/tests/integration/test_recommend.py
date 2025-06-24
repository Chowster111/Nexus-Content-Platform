# tests/integration/test_recommend.py
import pytest

@pytest.mark.asyncio
async def test_get_recommendations(client):
    response = await client.get("/find/recommend", params={"query": "AI"})
    assert response.status_code == 200
    body = response.json()
    assert "results" in body
    assert isinstance(body["results"], list)
