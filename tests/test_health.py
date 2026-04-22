def test_system_health(client):
    res = client.get('/health')

    assert res.status_code == 200
    data = res.get_json()

    assert data["status"] == "success"
    assert data["data"]["status"] == "UP"
    assert data["data"]["database"] == "CONNECTED"