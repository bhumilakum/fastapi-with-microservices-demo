from app.core.database import engine
from fastapi import FastAPI
from app.schemas import models

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.get("/")
async def index():
    return {"Real": "Python"}
