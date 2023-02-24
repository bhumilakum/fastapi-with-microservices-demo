from datetime import date

from app.schemas import models, schemas_training_session, schemas_user
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import func

# from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def get_training_session_query(id, db):
    training_session_query = db.query(models.TrainingSession).filter(
        models.TrainingSession.id == id
    )
    if training_session_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The training session with the ID {id} is not found!",
        )
    return training_session_query, training_session_query.first()


def get_time_difference_in_minute(start_time, end_time):
    time_diff = int((end_time - start_time).total_seconds() / 60)
    return time_diff


def validate_session_timing(start_time, end_time):
    if start_time > end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session timings!"
        )


def get_all(
    db: Session,
    current_user: schemas_user.User,
    session_filter: str,
    skip: int,
    limit: int,
):
    try:
        filter_dict = []
        order_dict = [models.TrainingSession.start_time.desc()]
        if session_filter is not None:
            if session_filter == "today":
                filter_dict = [
                    func.DATE(models.TrainingSession.start_time) == date.today()
                ]
                order_dict = [models.TrainingSession.start_time]
            elif session_filter == "past":
                filter_dict = [
                    func.DATE(models.TrainingSession.start_time) < date.today()
                ]
                order_dict = [models.TrainingSession.start_time.desc()]
            elif session_filter == "upcoming":
                filter_dict = [
                    func.DATE(models.TrainingSession.start_time) > date.today()
                ]
                order_dict = [models.TrainingSession.start_time]
            elif session_filter == "my_sessions":
                if current_user.user_type.name in ["admin", "mentor"]:
                    filter_dict = [models.TrainingSession.presenter == current_user]
                    order_dict = [models.TrainingSession.start_time]
                elif current_user.user_type.name == "trainee":
                    filter_dict = [
                        models.TrainingSession.attendees.contains(current_user)
                    ]
                else:
                    pass
            else:
                pass

        training_sessions = (
            db.query(models.TrainingSession)
            .filter(*filter_dict)
            .order_by(*order_dict)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return {"training_session": training_sessions, "skip": skip, "limit": limit}
    except Exception as e:
        print("Error in getting all training session. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def show(id: int, db: Session):
    training_session_query, training_session = get_training_session_query(id, db)

    return training_session


def create(request: schemas_training_session.CreateTrainingSession, db: Session):
    try:
        validate_session_timing(request.start_time, request.end_time)

        total_time = get_time_difference_in_minute(request.start_time, request.end_time)

        if "attendees" in request.dict(exclude_unset=True):
            attendees = (
                db.query(models.User)
                .filter(models.User.id.in_(request.attendees))
                .all()
            )
            if attendees is not None:
                request.attendees = attendees
                request.present_attendees = len(attendees)

        new_session = models.TrainingSession(**request.dict(), total_time=total_time)

        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session
    except Exception as e:
        print("Error in creating a training session. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def update(
    id: int, request: schemas_training_session.UpdateTrainingSession, db: Session
):
    training_session_query, training_session = get_training_session_query(id, db)

    if "start_time" in request.dict(exclude_unset=True) or "end_time" in request.dict(
        exclude_unset=True
    ):
        start_time = (
            request.start_time
            if "start_time" in request.dict(exclude_unset=True)
            else training_session.start_time
        )
        end_time = (
            request.end_time
            if "end_time" in request.dict(exclude_unset=True)
            else training_session.end_time
        )

        validate_session_timing(start_time, end_time)
        total_time = get_time_difference_in_minute(start_time, end_time)
        request.total_time = total_time

    if "attendees" in request.dict(exclude_unset=True):
        attendees = (
            db.query(models.User).filter(models.User.id.in_(request.attendees)).all()
        )
        if attendees is not None:
            training_session.attendees = attendees
            training_session.present_attendees = len(attendees)
        delattr(request, "attendees")

    if request.dict(exclude_unset=True):
        training_session_query.update(request.dict(exclude_unset=True))

    db.commit()
    db.refresh(training_session)

    return training_session


def delete(id: int, db: Session):
    training_session_query, training_session = get_training_session_query(id, db)

    training_session_query.delete()
    db.commit()

    return JSONResponse(content={"message": "The training session has been deleted!"})
