from app.authentication import oauth2
from app.authentication.password_hashing import Hash
from app.core import database
from app.schemas import schemas
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.api import training_assignment


router = APIRouter(prefix="/training_assignment", tags=["TrainingAssignments"])


@router.get("/", response_model=schemas.ShowUser)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
):
    return training_assignment.get_all(db)


@router.get("/{id}", response_model=schemas.ShowUser)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
):
    return training_assignment.show(id, db)


@router.post("/create", response_model=schemas.ShowUser)
def create(
    request: schemas.User,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
):
    return training_assignment.create(request, db)


@router.patch("/{id}", response_model=schemas.ShowUser)
def update(
    id: int,
    request: schemas.User,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
):
    return training_assignment.update(id, request, db)


@router.delete("/{id}", response_model=schemas.ShowUser)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
):
    return training_assignment.delete(id, db)