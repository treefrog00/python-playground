def test_get_fish(client):
    response = client.get('/fish')

    assert response.status_code == 200
    data = response.get_json()
    assert data["data"][0]["AssociationRef"] == None

def test_post_to_the_postman(client):
    response = client.post('/postman', json=dict(strongbad="very yes"))

    assert response.status_code == 200
    assert response.get_json()["data"]["strongbad"] == "very yes"