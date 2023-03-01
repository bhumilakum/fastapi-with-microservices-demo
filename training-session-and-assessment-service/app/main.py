from app.core.config import settings
from app.core.database import engine
from app.routers import assignment, authentication, submission, training_session, user
from app.schemas import models
from fastapi import FastAPI

app = FastAPI(
    title=settings.APPLICATION_TITLE,
)

models.Base.metadata.create_all(engine)

# include all routers
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(training_session.router)
app.include_router(assignment.router)
app.include_router(submission.router)
