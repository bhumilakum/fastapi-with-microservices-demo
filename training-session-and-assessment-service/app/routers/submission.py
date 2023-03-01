from typing import Union

from app.api import api_submission
from app.authentication import oauth2
from app.core import database
from app.schemas import schemas_submission, schemas_user
from app.schemas.enums import SubmissionFilter
from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/assignment_submission", tags=["AssignmentSubmission"])


@router.get("/", response_model=schemas_submission.ShowSubmissionList)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
    session: Union[int, None] = None,
    assignment: Union[int, None] = None,
    user: Union[int, None] = None,
    skip: int = 0,
    limit: int = 50,
):
    return api_submission.get_all(
        db, current_user, session, assignment, user, skip, limit
    )


@router.get(
    "/trainee_submission", response_model=schemas_submission.ShowTraineeSubmissionList
)
def get_my_submission(
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["trainee"]
    ),
    submission_filter: SubmissionFilter = None,
    session: Union[int, None] = None,
    skip: int = 0,
    limit: int = 50,
):
    return api_submission.get_my_submission(
        db, current_user, submission_filter, session, skip, limit
    )


@router.get("/{id}", response_model=schemas_submission.ShowSubmission)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
):
    return api_submission.show(id, db, current_user)


@router.post(
    "/create",
    response_model=schemas_submission.ShowSubmissionFew,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: schemas_submission.CreateSubmission,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["trainee"]
    ),
):
    return api_submission.create(request, db, current_user)


@router.patch(
    "/my_submission/{id}", response_model=schemas_submission.ShowSubmissionFew
)
def update_trainee_submission(
    id: int,
    request: schemas_submission.UpdateTraineeSubmission,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["trainee"]
    ),
):
    return api_submission.update_trainee_submission(id, request, db, current_user)


@router.patch("/{id}", response_model=schemas_submission.ShowSubmission)
def update(
    id: int,
    request: schemas_submission.UpdateSubmission,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_submission.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
):
    return api_submission.delete(id, db, current_user)
