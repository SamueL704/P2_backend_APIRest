from fastapi import APIRouter

router = APIRouter()

@router.get("/produtos")
def getAll_produtos():
    return

@router.post("/produtos")
def create_produto():
    return

@router.get("/produtos/{id}")
def get_produto():
    return

@router.delete("/produtos/{id}")
def delete_produto():
    return