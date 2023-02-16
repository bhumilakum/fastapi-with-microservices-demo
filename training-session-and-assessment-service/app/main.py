from app.core.database import engine
from app.routers import (
    assignment_grade,
    authentication,
    training_assignment,
    training_session,
    user,
)
from app.schemas import models
from fastapi import FastAPI

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(training_session.router)
app.include_router(training_assignment.router)
app.include_router(assignment_grade.router)


# @app.get("/")
# async def index():
#     return {"Real": "Python"}
