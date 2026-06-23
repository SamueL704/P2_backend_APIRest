# API de Produtos - FastAPI, PostgreSQL e Pytest

Projeto desenvolvido para a atividade avaliativa de Desenvolvimento de APIs com FastAPI.

A aplicação implementa uma API REST para gerenciamento de produtos de um pequeno e-commerce, utilizando FastAPI, SQLAlchemy ORM, Pydantic, PostgreSQL via Docker e testes automatizados com Pytest.

## Tecnologias utilizadas

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* PostgreSQL
* Docker Compose
* Pytest
* TestClient
* pytest-cov

## Estrutura do projeto

```text
P2_backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── repository.py
│   ├── routes.py
│   └── schemas.py
├── tests/
│   ├── __init__.py
│   └── test_produtos.py
├── conftest.py
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Funcionalidades da API

A API possui os seguintes endpoints:

```text
GET /produtos
```

Lista todos os produtos cadastrados.

```text
POST /produtos
```

Cria um novo produto.

```text
GET /produtos/{id}
```

Busca um produto pelo ID. Caso o produto não exista, retorna erro 404.

```text
DELETE /produtos/{id}
```

Remove um produto pelo ID. Caso o produto não exista, retorna erro 404.

## Modelo de Produto

O produto possui os seguintes campos:

```text
id       - inteiro, chave primária gerada automaticamente
nome     - texto obrigatório, não pode ser vazio
preco    - número obrigatório, deve ser maior que zero
estoque  - inteiro, padrão 0
ativo    - booleano, padrão True
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as URLs dos bancos de dados:

```env
DATABASE_URL=postgresql+psycopg2://samuel:samuel123@localhost:5432/product_db
TEST_DATABASE_URL=postgresql+psycopg2://samuel:samuel123@localhost:5433/product_test_db
```

A variável `DATABASE_URL` é usada pela API em ambiente de desenvolvimento.

A variável `TEST_DATABASE_URL` é usada pelos testes automatizados com Pytest.

## Subindo o banco de teste com Docker

Antes de executar os testes, suba o banco PostgreSQL exclusivo para testes:

```bash
docker-compose up -d db_test
```

Para verificar se os containers estão rodando:

```bash
docker-compose ps
```

O banco de desenvolvimento usa a porta `5432`.

O banco de teste usa a porta `5433`.

O banco de desenvolvimento possui volume persistente. Já o banco de teste não possui volume, pois seus dados são descartáveis.

## Executando a API em desenvolvimento

Para subir o banco de desenvolvimento:

```bash
docker-compose up -d db
```

Para iniciar a API:

```bash
uvicorn app.main:app --reload
```

A documentação interativa da API pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

## Executando os testes

Com o banco de teste rodando, execute:

```bash
pytest -v
```

Para executar os testes com relatório de cobertura:

```bash
pytest --cov=app -v
```

## Saída esperada dos testes

Ao executar:

```bash
pytest -v
```

A saída esperada é semelhante a:

```text
collected 14 items

tests/test_produtos.py::test_listar_produtos_banco_vazio PASSED
tests/test_produtos.py::test_criar_produto_retorna_201 PASSED
tests/test_produtos.py::test_criar_produto_verifica_persistencia PASSED
tests/test_produtos.py::test_criar_produto_aparece_na_listagem PASSED
tests/test_produtos.py::test_buscar_produto_por_id_sucesso PASSED
tests/test_produtos.py::test_buscar_produto_id_inexistente_retorna_404 PASSED
tests/test_produtos.py::test_deletar_produto_retorna_204 PASSED
tests/test_produtos.py::test_deletar_produto_confirma_remocao PASSED
tests/test_produtos.py::test_deletar_produto_inexistente_retorna_404 PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload0] PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload1] PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload2] PASSED
tests/test_produtos.py::test_criar_produto_payload_invalido_retorna_422[payload3] PASSED
tests/test_produtos.py::test_banco_esta_isolado_entre_testes PASSED

14 passed
```

Ao executar:

```bash
pytest --cov=app -v
```

A saída esperada de cobertura é semelhante a:

```text
Name                Stmts   Miss  Cover
---------------------------------------
app\__init__.py         0      0   100%
app\database.py        22      5    77%
app\main.py            10      1    90%
app\models.py          10      0   100%
app\repository.py      15      0   100%
app\routes.py          24      0   100%
app\schemas.py         13      0   100%
---------------------------------------
TOTAL                  94      6    94%

14 passed
```

## Como funciona o isolamento entre testes

Os testes utilizam uma fixture chamada `client`, definida no arquivo `conftest.py`.

Essa fixture cria uma conexão separada com o banco de teste, usando a variável `TEST_DATABASE_URL`.

Antes de cada teste, a fixture executa:

```python
Base.metadata.drop_all(bind=engine_test)
Base.metadata.create_all(bind=engine_test)
```

Isso apaga as tabelas antigas do banco de teste e cria tabelas novas, garantindo que cada teste comece com o banco limpo.

Durante os testes, o FastAPI usa:

```python
app.dependency_overrides[get_db] = override_get_db
```

Esse comando substitui a dependência original `get_db`, que usa o banco de desenvolvimento, por uma dependência de teste, que usa o banco da porta `5433`.

Depois que o teste termina, a fixture executa novamente:

```python
Base.metadata.drop_all(bind=engine_test)
```

Assim, os dados criados em um teste não interferem nos outros testes.

Esse isolamento garante que os testes possam ser executados em qualquer ordem sem depender do estado deixado por testes anteriores.

## Casos testados

A suíte de testes cobre:

* Listagem de produtos com banco vazio
* Criação de produto com status 201
* Persistência do produto criado no banco
* Produto criado aparecendo na listagem
* Busca por ID com sucesso
* Busca por ID inexistente retornando 404
* Remoção de produto retornando 204
* Confirmação de remoção com GET subsequente
* Remoção de produto inexistente retornando 404
* Validação de payloads inválidos retornando 422
* Isolamento do banco entre testes

## Comando final de verificação

Antes da entrega, execute:

```bash
docker-compose up -d db_test
pytest --cov=app -v
```

Se todos os testes passarem e a cobertura estiver acima de 85%, o projeto está pronto para entrega.
