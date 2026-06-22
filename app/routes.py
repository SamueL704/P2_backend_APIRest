from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import repository
from app.schemas import ProdutoResponse, ProdutoCreate

router = APIRouter()

@router.get("/produtos", response_model=list[ProdutoResponse])
def get_all_products(db: Session = Depends(get_db)):
    return repository.get_all_products(db)

@router.get("/produtos/{id}", response_model=ProdutoResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = repository.get_by_id(db, id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Produto não encontrado"
        )
    return product

@router.post("/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create_product(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return repository.create_product(db, produto)

@router.delete("/produtos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(id: int, db: Session = Depends(get_db)):
    product = repository.get_by_id(db, id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    repository.delete_product(db, product)