import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.main import app as fastapi_app
from app.database import Base, get_db
import app.models


def get_dbtest_url():
    url = os.getenv("TEST_DATABASE_URL")

    if not url:
        raise ValueError("TEST_DATABASE_URL não encontrada")
    
    return url

engine_test = create_engine(get_dbtest_url())

TestingSessionLocal = sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False
)


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fastapi_app) as test_client:
        yield test_client

    fastapi_app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture
def produto_existente(client):
    payload = {
        "nome": "Mouse",
        "preco": 50.0,
        "estoque": 10,
        "ativo": True
    }

    response = client.post("/produtos", json=payload)

    return response.json()