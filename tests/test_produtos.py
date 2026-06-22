def test_listar_produtos(client):
    response = client.get("/produtos")

    assert response.status_code == 200