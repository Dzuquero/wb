
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_short_link():
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_id" in data


def test_redirect_and_stats():
    create = client.post("/shorten", json={"url": "https://example.com"})
    short_id = create.json()["short_id"]

    r = client.get(f"/{short_id}", allow_redirects=False)
    assert r.status_code in (307, 302)

    stats = client.get(f"/stats/{short_id}")
    assert stats.status_code == 200
    assert stats.json()["clicks"] >= 1
