import pytest


def test_listar_produtos_banco_vazio(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto_retorna_201(client):
    payload = {
        "nome": "Teclado",
        "preco": 150.0,
        "estoque": 5,
        "ativo": True
    }

    response = client.post("/produtos", json=payload)

    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["nome"] == "Teclado"
    assert response.json()["preco"] == 150.0
    assert response.json()["estoque"] == 5
    assert response.json()["ativo"] is True


def test_criar_produto_verifica_persistencia(client):
    payload = {
        "nome": "Monitor",
        "preco": 800.0,
        "estoque": 3,
        "ativo": True
    }

    response_create = client.post("/produtos", json=payload)
    produto_criado = response_create.json()

    response_get = client.get(f"/produtos/{produto_criado['id']}")

    assert response_get.status_code == 200
    assert response_get.json()["id"] == produto_criado["id"]
    assert response_get.json()["nome"] == "Monitor"


def test_criar_produto_aparece_na_listagem(client):
    payload = {
        "nome": "Mousepad",
        "preco": 35.0,
        "estoque": 20,
        "ativo": True
    }

    client.post("/produtos", json=payload)

    response = client.get("/produtos")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "Mousepad"


def test_buscar_produto_por_id_sucesso(client, produto_existente):
    produto_id = produto_existente["id"]

    response = client.get(f"/produtos/{produto_id}")

    assert response.status_code == 200
    assert response.json()["id"] == produto_id
    assert response.json()["nome"] == produto_existente["nome"]


def test_buscar_produto_id_inexistente_retorna_404(client):
    response = client.get("/produtos/999")

    assert response.status_code == 404


def test_deletar_produto_retorna_204(client, produto_existente):
    produto_id = produto_existente["id"]

    response = client.delete(f"/produtos/{produto_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_deletar_produto_confirma_remocao(client, produto_existente):
    produto_id = produto_existente["id"]

    response_delete = client.delete(f"/produtos/{produto_id}")
    response_get = client.get(f"/produtos/{produto_id}")

    assert response_delete.status_code == 204
    assert response_get.status_code == 404


def test_deletar_produto_inexistente_retorna_404(client):
    response = client.delete("/produtos/999")

    assert response.status_code == 404


@pytest.mark.parametrize("payload", [
    {"nome": "", "preco": 100.0, "estoque": 5, "ativo": True},
    {"nome": "Produto sem preço", "estoque": 5, "ativo": True},
    {"nome": "Produto preço zero", "preco": 0, "estoque": 5, "ativo": True},
    {"nome": "Produto preço negativo", "preco": -10.0, "estoque": 5, "ativo": True},
])
def test_criar_produto_payload_invalido_retorna_422(client, payload):
    response = client.post("/produtos", json=payload)

    assert response.status_code == 422


def test_banco_esta_isolado_entre_testes(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert response.json() == []