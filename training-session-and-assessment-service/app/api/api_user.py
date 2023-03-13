from app.authentication.password_hashing import Hash
from app.core.email_service import send_email_background
from app.schemas import models, schemas_user
from fastapi import BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


def get_user_query(id: int, db: Session):
    user_query = db.query(models.User).filter(models.User.id == id)
    if user_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with the ID {id} is not found!",
        )
    return user_query, user_query.first()


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
    user_query, user = get_user_query(id, db)
    return user


def create(
    request: schemas_user.CreateUser, db: Session, background_tasks: BackgroundTasks
):
    try:
        request.password = Hash.bcrypt(request.password)
        new_user = models.User(**request.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # send a welcome email to the user
        body = {
            "username": f"{new_user.first_name} {new_user.last_name}"
            if new_user.first_name
            else "There"
        }
        data_dict = {"email": [new_user.email], "body": body}
        send_email_background(background_tasks, "Welcome!", data_dict)

        return new_user
    except Exception as e:
        print("Error in creating a user. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def update(id: int, request: schemas_user.UpdateUser, db: Session):
    user_query, user = get_user_query(id, db)

    user_query.update(request.dict(exclude_unset=True))
    db.commit()
    db.refresh(user)

    return user


def delete(id: int, db: Session):
    user_query, user = get_user_query(id, db)

    user_query.delete()
    db.commit()

    return JSONResponse(content={"message": "The user has been deleted!"})
