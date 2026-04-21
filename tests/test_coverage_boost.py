def test_register_missing_all_fields(client):
    res = client.post('/register', json={})
    assert res.status_code == 400


def test_register_missing_username(client):
    res = client.post('/register', json={
        "email": "a@mail.com",
        "password": "123"
    })
    assert res.status_code == 400


def test_register_missing_email(client):
    res = client.post('/register', json={
        "username": "abc",
        "password": "123"
    })
    assert res.status_code == 400


def test_login_missing_username(client):
    res = client.post('/login', json={
        "password": "123"
    })
    assert res.status_code == 400


def test_login_missing_password(client):
    res = client.post('/login', json={
        "username": "abc"
    })
    assert res.status_code == 400


def test_search_missing_q_param(client):
    res = client.get('/search')
    assert res.status_code == 400


def test_search_whitespace(client):
    res = client.get('/search?q=   ')
    assert res.status_code == 400


def test_students_empty_db(client):
    res = client.get('/students')
    assert res.status_code == 200
    assert "data" in res.get_json()


def test_update_no_data(client):
    client.post('/students', json={
        "username": "u1",
        "email": "u1@mail.com",
        "password": "123"
    })

    student = client.get('/students').get_json()["data"][-1]

    res = client.put(f'/students/{student["id"]}', json={})
    assert res.status_code == 200


def test_delete_flow(client):
    client.post('/students', json={
        "username": "deluser",
        "email": "del@mail.com",
        "password": "123"
    })

    student = client.get('/students').get_json()["data"][-1]

    res = client.delete(f'/students/{student["id"]}')
    assert res.status_code == 200