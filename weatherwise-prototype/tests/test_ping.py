def test_ping(client):
    res = client.get("/api/ping")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
