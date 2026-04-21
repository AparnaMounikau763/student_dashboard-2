def test_login_missing_fields(client):
    res = client.post('/login', json={})
    assert res.status_code in [400, 401]


def test_login_wrong_password(client):
    client.post('/register', json={
        "username": "testuser",
        "email": "test@mail.com",
        "password": "123"
    })

    res = client.post('/login', json={
        "username": "testuser",
        "password": "wrong"
    })

    assert res.status_code == 401