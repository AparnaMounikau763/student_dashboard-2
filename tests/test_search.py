def test_search_missing_query(client):
    res = client.get('/search')
    assert res.status_code == 400


def test_search_empty_string(client):
    res = client.get('/search?q=')
    assert res.status_code == 400