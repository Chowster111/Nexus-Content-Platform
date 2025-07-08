import pytest
import httpx

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_top_liked_articles():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/analytics/top-liked-articles")
        assert response.status_code == 200
        data = response.json()
        assert "top_liked_articles" in data
        assert isinstance(data["top_liked_articles"], list)
        # Optionally check structure if data exists
        if data["top_liked_articles"]:
            article = data["top_liked_articles"][0]
            assert "title" in article
            assert "url" in article
            assert "like_count" in article

@pytest.mark.asyncio
async def test_top_liked_categories():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/analytics/top-liked-categories")
        assert response.status_code == 200
        data = response.json()
        assert "top_liked_categories" in data
        assert isinstance(data["top_liked_categories"], list)
        # Optionally check structure if data exists
        if data["top_liked_categories"]:
            category = data["top_liked_categories"][0]
            assert isinstance(category, list) or isinstance(category, tuple)
            assert len(category) == 2  # [category, like_count] 