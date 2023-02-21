from sqlalchemy.orm import Session
from app.schemas import models, schemas
from fastapi import HTTPException, status
from app.authentication.password_hashing import Hash


def get_all(db: Session):
    pass

def show(id: int, db: Session):
    pass

def create(request: schemas.ShowUser, db: Session):
    new_user = models.User(
        email=request.email,
        password=Hash.bcrypt(request.password),
        user_type=request.user_type,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update(id: int, request: schemas.User, db: Session):
    pass

def delete(id: int, db: Session):
    pass

