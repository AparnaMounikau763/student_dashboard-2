import uuid

def test_get_student_not_found(client):
    res = client.get('/students/99999')
    assert res.status_code == 404


def test_delete_student_not_found(client):
    res = client.delete('/students/99999')
    assert res.status_code == 404


def test_update_duplicate_username(client):
    uid = str(uuid.uuid4())[:6]

    client.post('/students', json={
        "username": "userA",
        "email": f"{uid}@mail.com",
        "password": "123"
    })

    student = client.get('/students').get_json()["data"][-1]
    student_id = student["id"]

    client.post('/students', json={
        "username": "userB",
        "email": f"b_{uid}@mail.com",
        "password": "123"
    })

    res = client.put(f'/students/{student_id}', json={
        "username": "userB"
    })

    assert res.status_code == 400


def test_update_duplicate_email(client):
    uid = str(uuid.uuid4())[:6]

    client.post('/students', json={
        "username": "userC",
        "email": f"{uid}@mail.com",
        "password": "123"
    })

    student = client.get('/students').get_json()["data"][-1]
    student_id = student["id"]

    client.post('/students', json={
        "username": "userD",
        "email": f"d_{uid}@mail.com",
        "password": "123"
    })

    res = client.put(f'/students/{student_id}', json={
        "email": f"d_{uid}@mail.com"
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
        "username": "dup_user",
        "email": "dup1@mail.com",
        "password": "123"
    })

    res = client.post('/students', json={
        "username": "dup_user",
        "email": "new@mail.com",
        "password": "123"
    })

    assert res.status_code == 400


def test_post_student_duplicate_email(client):
    client.post('/students', json={
        "username": "user1",
        "email": "same@mail.com",
        "password": "123"
    })

    res = client.post('/students', json={
        "username": "user2",
        "email": "same@mail.com",
        "password": "123"
    })

    assert res.status_code == 400