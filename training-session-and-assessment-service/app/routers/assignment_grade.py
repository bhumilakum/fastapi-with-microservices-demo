from app.api import assignment_grade
from app.authentication import oauth2
from app.core import database
from app.schemas import schemas
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

router = APIRouter(prefix="/assignment_grade", tags=["AssignmentGrade"])


@router.get("/", response_model=schemas.ShowUser)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return assignment_grade.get_all(db)


@router.get("/{id}", response_model=schemas.ShowUser)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return assignment_grade.show(id, db)


@router.post("/create", response_model=schemas.ShowUser)
def create(
    request: schemas.User,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return assignment_grade.create(request, db)


@router.patch("/{id}", response_model=schemas.ShowUser)
def update(
    id: int,
    request: schemas.User,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return assignment_grade.update(id, request, db)


@router.delete("/{id}", response_model=schemas.ShowUser)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return assignment_grade.delete(id, db)
