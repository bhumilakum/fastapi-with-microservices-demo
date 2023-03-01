from datetime import date
from typing import Union

from app.api import api_assignment
from app.authentication import oauth2
from app.core import database
from app.schemas import schemas_assignment, schemas_user
from app.schemas.enums import AssignmentFilter
from fastapi import APIRouter, Depends, Query, Security, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/training_assignment", tags=["TrainingAssignments"])


@router.get("/", response_model=schemas_assignment.ShowAssignmentList)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
    title: Union[str, None] = None,
    given_date: Union[date, None] = Query(
        default=None, description="format: YYYY-MM-DD"
    ),
    due_date: Union[date, None] = Query(default=None, description="format: YYYY-MM-DD"),
    session: Union[int, None] = None,
    skip: int = 0,
    limit: int = 50,
):
    return api_assignment.get_all(
        db, current_user, title, given_date, due_date, session, skip, limit
    )


@router.get("/trainee_report", response_model=schemas_assignment.ShowAssignmentList)
def show_trainee_report(
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["trainee"]
    ),
    assignment_filter: AssignmentFilter = AssignmentFilter.submitted_assignment,
    skip: int = 0,
    limit: int = 50,
):
    return api_assignment.trainee_assignment(
        db, current_user, assignment_filter, skip, limit
    )


@router.get("/{id}", response_model=schemas_assignment.ShowAssignment)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
):
    return api_assignment.show(id, db)


@router.post(
    "/create",
    response_model=schemas_assignment.ShowAssignment,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: schemas_assignment.CreateAssignment,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_assignment.create(request, db)


@router.patch("/{id}", response_model=schemas_assignment.ShowAssignment)
def update(
    id: int,
    request: schemas_assignment.UpdateAssignment,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_assignment.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_assignment.delete(id, db)
