# tests/integration/test_search.py
import pytest

@pytest.mark.asyncio
async def test_search_articles(client):
    response = await client.get("/search/articles", params={"q": "machine learning"})
    assert response.status_code == 200
    body = response.json()
    assert "results" in body
    assert isinstance(body["results"], list)
    if body["results"]:
        assert "title" in body["results"][0]
        assert "url" in body["results"][0]
