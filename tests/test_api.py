def test_get_student_by_id(client):
    res = client.post('/students', json={
        "username": "single_user",
        "email": "single@mail.com",
        "password": "123"
    })

    students = client.get('/students').get_json()["data"]
    student_id = students[-1]["id"]

    res = client.get(f'/students/{student_id}')
    assert res.status_code == 200


def test_get_student_invalid_id(client):
    res = client.get('/students/999999')
    assert res.status_code == 404


def test_update_email(client):
    client.post('/students', json={
        "username": "email_user",
        "email": "email@mail.com",
        "password": "123"
    })

    student_id = client.get('/students').get_json()["data"][-1]["id"]

    res = client.put(f'/students/{student_id}', json={
        "email": "new@mail.com"
    })

    assert res.status_code == 200


def test_register_missing_fields_partial(client):
    res = client.post('/register', json={"username": "only"})
    assert res.status_code == 400