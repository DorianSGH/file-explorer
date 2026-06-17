"""Health endpoint — sanity check that the app starts up correctly."""


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
