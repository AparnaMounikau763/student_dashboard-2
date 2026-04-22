def test_register_missing_payload(client):
    res = client.post('/register', json=None)
    assert res.status_code == 400


def test_login_missing_payload(client):
    res = client.post('/login', json=None)
    assert res.status_code == 400


def test_search_none_query(client):
    res = client.get('/search')
    assert res.status_code == 400


def test_search_empty_query(client):
    res = client.get('/search?q=')
    assert res.status_code == 400


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
        "username": "del_user",
        "email": "del@mail.com",
        "password": "123"
    })

    student = client.get('/students').get_json()["data"][-1]

    res = client.delete(f'/students/{student["id"]}')
    assert res.status_code == 200


def test_update_not_found(client):
    res = client.put('/students/9999', json={"username": "x"})
    assert res.status_code == 404


def test_delete_not_found(client):
    res = client.delete('/students/9999')
    assert res.status_code == 404