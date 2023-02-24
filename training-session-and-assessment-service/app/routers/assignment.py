from datetime import date
from typing import Union

from app.api import assignment
from app.authentication import oauth2
from app.core import database
from app.schemas import schemas
from fastapi import APIRouter, Depends, Query, Security, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/training_assignment", tags=["TrainingAssignments"])


@router.get("/", response_model=schemas.ShowAssignmentList)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
    title: Union[str, None] = None,
    given_date: Union[date, None] = Query(
        default=None, description="format: YYYY-MM-DD"
    ),
    due_date: Union[date, None] = Query(default=None, description="format: YYYY-MM-DD"),
    skip: int = 0,
    limit: int = 50,
):
    return assignment.get_all(
        db, current_user, title, given_date, due_date, skip, limit
    )


@router.get("/{id}", response_model=schemas.ShowAssignment)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor", "trainee"]
    ),
):
    return assignment.show(id, db)


@router.post(
    "/create",
    response_model=schemas.ShowAssignment,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: schemas.CreateAssignment,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return assignment.create(request, db)


@router.patch("/{id}", response_model=schemas.ShowAssignment)
def update(
    id: int,
    request: schemas.UpdateAssignment,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return assignment.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return assignment.delete(id, db)
