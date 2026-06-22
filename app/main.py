from fastapi import FastAPI

from app.models import Produto
from app.database import criar_tabelas

from app.routes import router


app = FastAPI()

@router.get("/")
def home():
    return {"message":"api rodando"}

app.include_router(router)


criar_tabelas()