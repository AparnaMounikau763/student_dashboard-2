def test_search(client):
    client.post('/register', json={
        "username": "Aparna",
        "email": "aparna@gmail.com",
        "password": "Aparna123"
    })

    # valid search
    res = client.get('/search?q=Aparna')
    assert res.status_code == 200

    # empty query branch
    res = client.get('/search?q=')
    assert res.status_code == 400

    # missing query branch
    res = client.get('/search')
    assert res.status_code == 400


# 🔥 extra edge case
def test_search_whitespace(client):
    res = client.get('/search?q=   ')
    assert res.status_code == 400