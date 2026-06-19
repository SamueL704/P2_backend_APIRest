from fastapi import FastAPI
import models
from database import Base, engine
from routes import router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)