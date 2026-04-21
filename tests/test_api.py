def test_get_student_not_found(client):
    res = client.get('/students/99999')
    assert res.status_code == 404


def test_delete_student_not_found(client):
    res = client.delete('/students/99999')
    assert res.status_code == 404


def test_update_duplicate_username(client):
    uid = "u1"

    client.post('/students', json={
        "username": "userA",
        "email": "a@mail.com",
        "password": "123"
    })

    student = client.get('/students').get_json()["data"][-1]

    client.post('/students', json={
        "username": "userB",
        "email": "b@mail.com",
        "password": "123"
    })

    res = client.put(f'/students/{student["id"]}', json={
        "username": "userB"
    })

    assert res.status_code == 400


def test_update_duplicate_email(client):
    client.post('/students', json={
        "username": "userC",
        "email": "c@mail.com",
        "password": "123"
    })

    student = client.get('/students').get_json()["data"][-1]

    client.post('/students', json={
        "username": "userD",
        "email": "d@mail.com",
        "password": "123"
    })

    res = client.put(f'/students/{student["id"]}', json={
        "email": "d@mail.com"
    })

    assert res.status_code == 400


def test_get_all_students(client):
    res = client.get('/students')
    assert res.status_code == 200
    assert "data" in res.get_json()


def test_post_student_missing_fields(client):
    res = client.post('/students', json={})
    assert res.status_code == 400


def test_post_student_duplicate_username(client):
    client.post('/students', json={
        "username": "dup",
        "email": "dup1@mail.com",
        "password": "123"
    })

    res = client.post('/students', json={
        "username": "dup",
        "email": "new@mail.com",
        "password": "123"
    })

    assert res.status_code == 400


def test_post_student_duplicate_email(client):
    client.post('/students', json={
        "username": "u1",
        "email": "same@mail.com",
        "password": "123"
    })

    res = client.post('/students', json={
        "username": "u2",
        "email": "same@mail.com",
        "password": "123"
    })

    assert res.status_code == 400