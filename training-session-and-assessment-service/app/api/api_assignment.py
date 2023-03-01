from datetime import date

from app.schemas import models, schemas_assignment, schemas_user
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


def get_assignment_query(id, db):
    assignment_query = db.query(models.Assignment).filter(models.Assignment.id == id)
    if assignment_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The session assignment with the ID {id} is not found!",
        )
    return assignment_query, assignment_query.first()


def validate_submission_dates(given_date, due_date):
    if given_date > due_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid assignment submission dates!",
        )


def validate_assignment_score(total_score, passing_score):
    if passing_score > total_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Total score should be grater than passing score of an assignment!",
        )


def get_all(
    db: Session,
    current_user: schemas_user.User,
    title: str,
    given_date: date,
    due_date: date,
    session: int,
    skip: int,
    limit: int,
):
    try:
        filter_dict = []
        order_dict = [models.Assignment.given_date.desc()]

        if title is not None:
            search_key = f"%{title}%"
            filter_dict.append(models.Assignment.title.like(search_key))
        if given_date is not None:
            filter_dict.append(models.Assignment.given_date == given_date)
        if due_date is not None:
            filter_dict.append(models.Assignment.due_date == due_date)
        if session is not None:
            filter_dict.append(models.Assignment.related_session == session)

        assignments = (
            db.query(models.Assignment)
            .filter(*filter_dict)
            .order_by(*order_dict)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return {"assignments": assignments, "skip": skip, "limit": limit}
    except Exception as e:
        print("Error in getting all assignments. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def trainee_assignment(
    db: Session,
    current_user: schemas_user.User,
    assignment_filter: str,
    skip: int,
    limit: int,
):
    try:
        filter_dict = []
        order_dict = [models.Assignment.given_date.desc()]

        submitted_assignment = (
            db.query(models.Assignment)
            .join(models.Submission)
            .filter(models.Submission.trainee_user == current_user)
            .order_by(*order_dict)
            .offset(skip)
            .limit(limit)
            .all()
        )

        if assignment_filter is not None:
            if assignment_filter == "submitted_assignment":
                assignments = submitted_assignment
            elif assignment_filter in ["pending_assignment", "due_assignment", "due_today"]:
                assignment_ids = [record.id for record in submitted_assignment]
                filter_dict = [~models.Assignment.id.in_(assignment_ids)]
                if assignment_filter == "due_assignment":
                    filter_dict.append(models.Assignment.due_date < date.today())
                if assignment_filter == "due_today":
                    filter_dict.append(models.Assignment.due_date == date.today())
                assignments = (
                    db.query(models.Assignment)
                    .filter(*filter_dict)
                    .order_by(*order_dict)
                    .offset(skip)
                    .limit(limit)
                    .all()
                )
            else:
                pass
        else:
            pass

        return {"assignments": assignments, "skip": skip, "limit": limit}
    except Exception as e:
        print("Error in getting all assignments. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def show(id: int, db: Session):
    assignment_query, assignment = get_assignment_query(id, db)
    return assignment


def create(request: schemas_assignment.CreateAssignment, db: Session):
    try:
        validate_submission_dates(request.given_date, request.due_date)
        validate_assignment_score(request.total_score, request.passing_score)

        new_assignment = models.Assignment(**request.dict())
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)

        return new_assignment
    except Exception as e:
        print("Error in creating an assignment.", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def update(id: int, request: schemas_assignment.UpdateAssignment, db: Session):
    assignment_query, assignment = get_assignment_query(id, db)

    if "given_date" in request.dict(exclude_unset=True) or "due_date" in request.dict(
        exclude_unset=True
    ):
        given_date = (
            request.given_date
            if "given_date" in request.dict(exclude_unset=True)
            else assignment.given_date
        )
        due_date = (
            request.due_date
            if "due_date" in request.dict(exclude_unset=True)
            else assignment.due_date
        )
        validate_submission_dates(given_date, due_date)

    if "total_score" in request.dict(
        exclude_unset=True
    ) or "passing_score" in request.dict(exclude_unset=True):
        total_score = (
            request.total_score
            if "total_score" in request.dict(exclude_unset=True)
            else assignment.total_score
        )
        passing_score = (
            request.passing_score
            if "passing_score" in request.dict(exclude_unset=True)
            else assignment.passing_score
        )
        validate_submission_dates(total_score, passing_score)

    assignment_query.update(request.dict(exclude_unset=True))
    db.commit()
    db.refresh(assignment)

    return assignment


def delete(id: int, db: Session):
    assignment_query, assignment = get_assignment_query(id, db)

    assignment_query.delete()
    db.commit()

    return JSONResponse(content={"message": "The session assignment has been deleted!"})
