from fastapi import FastAPI
import app.models as models
from database import criar_tabelas
from routes import router_produtos

criar_tabelas()

app = FastAPI()

app.include_router(router_produtos)