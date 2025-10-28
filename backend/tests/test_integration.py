def test_search_vendors_endpoint(client):
    """
    TODO implement test cases
    """
    response = client.post('/vendors/?page=1&page_size=10', json={})
    assert response.status_code == 200

