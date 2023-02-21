from app.schemas import models, schemas
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


def is_user_exists(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with the ID {id} is not found!",
        )
    return user


def get_all(db: Session, user_type: str, skip: int, limit: int):
    try:
        filter_dict = (
            [models.User.user_type == user_type] if user_type is not None else []
        )
        users = (
            db.query(models.User).filter(*filter_dict).offset(skip).limit(limit).all()
        )
        return {"users": users, "skip": skip, "limit": limit}
    except Exception as e:
        print("Error in getting all users. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def show(id: int, db: Session):
    user = is_user_exists(id, db)
    return user


def create(request: schemas.CreateUser, db: Session):
    try:
        new_user = models.User(**request.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print("Error in creating a user. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def update(id: int, request: schemas.UpdateUser, db: Session):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with the ID {id} is not found!",
        )

    user_query.update(request.dict(exclude_unset=True))
    db.commit()
    db.refresh(user)

    return user


def delete(id: int, db: Session):
    user = is_user_exists(id, db)

    db.delete(user)
    db.commit()

    return JSONResponse(content={"message": "The user has been deleted!"})
