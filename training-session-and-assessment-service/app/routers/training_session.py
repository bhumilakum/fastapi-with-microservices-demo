from typing import Optional

from app.api import training_session
from app.authentication import oauth2
from app.core import database
from app.schemas import schemas
from fastapi import APIRouter, Depends, Query, Security, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/training_session", tags=["TrainingSessions"])


@router.get("/", response_model=schemas.ShowTrainingSessionList)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
    session_filter: Optional[str] = Query(
        None,
        description="Session filter based on timimngs (today, past, upcoming)",
        regex=r"^\btoday\b$|^\bpast\b$|^\bupcoming\b$",
    ),
    skip: int = 0,
    limit: int = 50,
):
    return training_session.get_all(db, session_filter, skip, limit)


@router.get("/{id}", response_model=schemas.ShowTrainingSession)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
):
    return training_session.show(id, db)


@router.post(
    "/create",
    response_model=schemas.ShowTrainingSession,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: schemas.CreateTrainingSession,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return training_session.create(request, db)


@router.patch("/{id}", response_model=schemas.ShowTrainingSession)
def update(
    id: int,
    request: schemas.UpdateTrainingSession,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return training_session.update(id, request, db)


@router.delete("/{id}", response_model=schemas.ShowUser)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return training_session.delete(id, db)
