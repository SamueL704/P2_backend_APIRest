from pydantic import BaseModel, Field, ConfigDict


class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    estoque: int = 0
    ativo: bool = True


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)