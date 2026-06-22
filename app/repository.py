from sqlalchemy.orm import Session
from app.models import Produto

def get_all_products(db: Session):
    return db.query(Produto).all()

def get_by_id(db: Session, product_id):
    return db.get(Produto, product_id)

def create_product(db: Session, produto):
    new_product = Produto(**produto.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

def delete_product(db: Session, product):
    db.delete(product)
    db.commit()