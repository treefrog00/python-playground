def test_get_hello(client):
    response = client.get('/hello')

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "hello"

def test_post_form_data_hello(client):
    response = client.post('/hello', data=dict(
        name="Fitzgerald",
    ))

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Hello Fitzgerald"
