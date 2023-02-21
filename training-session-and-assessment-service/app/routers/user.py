from app.authentication import oauth2
from app.authentication.password_hashing import Hash
from app.core import database
from app.schemas import schemas
from fastapi import APIRouter, Depends, Security, Query, status
from sqlalchemy.orm import Session
from app.api import user
from typing import List, Union, Optional


router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/", response_model=schemas.ShowUserList)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
    user_type: Optional[str] = Query(None, description="User type wise filter (admin, mentor, trainee)", regex=r"^\badmin\b$|^\bmentor\b$|^\btrainee\b$"),
    skip: int = 0,
    limit: int = 50,
):
    return user.get_all(db, user_type, skip, limit)


@router.get("/{id}", response_model=schemas.ShowUser)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
):
    return user.show(id, db)


@router.post("/create", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.CreateUser,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
):
    return user.create(request, db)


@router.patch("/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int,
    request: schemas.UpdateUser,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin", "mentor"]),
):
    return user.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["admin"]),
):
    return user.delete(id, db)