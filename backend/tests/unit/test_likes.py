from fastapi.testclient import TestClient
from app import app  # your FastAPI app

client = TestClient(app)

def test_save_likes_endpoint(monkeypatch):
    def mock_insert_likes(request):
        return {"message": "Likes saved"}

    response = client.post("/user/likes", json={
        "user_id": "test-user",
        "likes": [{"url": "http://example.com", "liked": True}]
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Likes saved"}
