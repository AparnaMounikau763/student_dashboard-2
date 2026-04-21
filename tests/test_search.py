def test_search(client):
    client.post('/register', json={
        "username": "Aparna",
        "email": "aparna@gmail.com",
        "password": "Aparna123"
    })

    res = client.get('/search?q=Aparna')
    assert res.status_code == 200
    assert "Aparna" in res.get_data(as_text=True)


def test_search_no_query(client):
    res = client.get('/search')
    assert res.status_code == 400