from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_url():
    url = os.getenv("DATABASE_URL")

    if not url:
        raise ValueError("DATABASE_URL não encontrada")
    
    return url
        
engine = create_engine(get_db_url())

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas")