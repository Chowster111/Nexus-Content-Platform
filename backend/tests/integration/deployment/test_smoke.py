import httpx
import pytest

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_root_route():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        assert response.status_code == 200
        assert response.json().get("message") == "Engineering Blog Recommender API"

@pytest.mark.asyncio
async def test_search_route():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/search/articles?q=python")
        assert response.status_code == 200
        assert "results" in response.json()

@pytest.mark.asyncio
async def test_recommend_route():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/find/recommend?query=python&top_k=3")
        assert response.status_code == 200
        assert "results" in response.json()

@pytest.mark.asyncio
async def test_likes_post():
    async with httpx.AsyncClient() as client:
        payload = {
            "user_id": "test_user_deploy",
            "likes": [{"url": "https://example.com/test-article", "liked": True}],
        }
        response = await client.post(f"{BASE_URL}/user/likes", json=payload)
        assert response.status_code == 200
        assert response.json().get("message") == "Likes saved"
