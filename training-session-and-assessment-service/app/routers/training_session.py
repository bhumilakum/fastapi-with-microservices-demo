from app.api import api_training_session
from app.authentication import oauth2
from app.core import database
from app.schemas import schemas_training_session, schemas_user
from app.schemas.enums import TrainingSessionFilter
from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/training_session", tags=["TrainingSessions"])


@router.get("/", response_model=schemas_training_session.ShowTrainingSessionList)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
    # session_filter: Optional[str] = Query(
    #     None,
    #     description="Session filter based on timimngs (today, past, upcoming)",
    #     regex=r"^\btoday\b$|^\bpast\b$|^\bupcoming\b$|^\bmy_sessions\b$",
    # ),
    session_filter: TrainingSessionFilter = None,
    skip: int = 0,
    limit: int = 50,
):
    return api_training_session.get_all(db, current_user, session_filter, skip, limit)


@router.get("/{id}", response_model=schemas_training_session.ShowTrainingSession)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
):
    return api_training_session.show(id, db)


@router.post(
    "/create",
    response_model=schemas_training_session.ShowTrainingSession,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: schemas_training_session.CreateTrainingSession,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_training_session.create(request, db)


@router.patch("/{id}", response_model=schemas_training_session.ShowTrainingSession)
def update(
    id: int,
    request: schemas_training_session.UpdateTrainingSession,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_training_session.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_training_session.delete(id, db)
