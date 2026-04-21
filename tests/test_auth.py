import uuid

def test_register_duplicate_username(client):
    uid = str(uuid.uuid4())[:6]

    data = {
        "username": f"user_{uid}",
        "email": f"{uid}@mail.com",
        "password": "123"
    }

    client.post('/register', json=data)
    res = client.post('/register', json=data)

    assert res.status_code == 400


def test_register_duplicate_email(client):
    uid = str(uuid.uuid4())[:6]

    client.post('/register', json={
        "username": f"user1_{uid}",
        "email": f"{uid}@mail.com",
        "password": "123"
    })

    res = client.post('/register', json={
        "username": f"user2_{uid}",
        "email": f"{uid}@mail.com",
        "password": "123"
    })

    assert res.status_code == 400


def test_register_missing_fields(client):
    res = client.post('/register', json={})
    assert res.status_code == 400


def test_login_missing_fields(client):
    res = client.post('/login', json={})
    assert res.status_code == 400


def test_login_invalid(client):
    res = client.post('/login', json={
        "username": "wrong",
        "password": "wrong"
    })
    assert res.status_code == 401