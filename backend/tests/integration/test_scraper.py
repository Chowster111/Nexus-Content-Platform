# tests/integration/test_scraper.py
import pytest

@pytest.mark.asyncio
async def test_scrape_all_sources(client):
    response = await client.post("/scrape/all")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    for source, result in body.items():
        assert isinstance(result, dict)
        assert "status" in result or "error" in result
