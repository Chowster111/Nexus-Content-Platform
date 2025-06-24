# tests/integration/test_likes.py
import pytest

@pytest.mark.asyncio
async def test_post_likes(client):
    data = {
        "user_id": "test_user_123",
        "likes": [
            {"url": "https://example.com/test1", "liked": True},
            {"url": "https://example.com/test2", "liked": False},
        ],
    }
    response = await client.post("/user/likes", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Likes saved"
