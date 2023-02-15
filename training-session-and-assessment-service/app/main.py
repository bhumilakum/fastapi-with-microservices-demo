from app.core.database import engine
from app.schemas import models
from fastapi import FastAPI

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.get("/")
async def index():
    return {"Real": "Python"}
