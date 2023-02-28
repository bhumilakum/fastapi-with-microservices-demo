from datetime import date

from app.schemas import models, schemas_submission, schemas_user
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

# from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def get_submission_query(id, db, current_user=None):

    submission_query = db.query(models.Submission).filter(models.Submission.id == id)

    if submission_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The assignment submission with the ID {id} is not found!",
        )

    if current_user and current_user.user_type.name == "trainee":
        submission_query = submission_query.filter(
            models.Submission.trainee_user == current_user
        )
        if submission_query.first() is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions!",
            )

    return submission_query, submission_query.first()


def get_result(assignment, grades):
    trainee_score = sum(grades.values())
    if trainee_score > assignment.total_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Given score should not be grater than total score!",
        )

    result = "PASS" if trainee_score >= assignment.passing_score else "FAIL"

    return trainee_score, result


def get_all(
    db: Session,
    current_user: schemas_user.User,
    assignment: int,
    user: int,
    skip: int,
    limit: int,
):
    try:
        filter_dict = []
        order_dict = [models.Submission.submission_date.desc()]

        if assignment is not None:
            filter_dict.append(models.Submission.assignment_fk == assignment)
        if user is not None:
            filter_dict.append(models.Submission.user_fk == user)

        submissions = (
            db.query(models.Submission)
            .filter(*filter_dict)
            .order_by(*order_dict)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return {"submissions": submissions, "skip": skip, "limit": limit}
    except Exception as e:
        print("Error in getting all submissions. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def get_my_submission(
    db: Session,
    current_user: schemas_user.User,
    submission_filter: str,
    session: int,
    skip: int,
    limit: int,
):
    try:
        filter_dict = [models.Submission.trainee_user == current_user]
        order_dict = [models.Submission.submission_date.desc()]

        if submission_filter is not None:
            if submission_filter == "submitted_today":
                filter_dict.append(models.Submission.submission_date == date.today())
            elif submission_filter == "graded_submission":
                filter_dict.append(models.Submission.result != None)  # noqa
            elif submission_filter == "pending_to_grade":
                filter_dict.append(models.Submission.result == None)  # noqa
            elif submission_filter == "submission_result_PASS":
                filter_dict.append(models.Submission.result == "PASS")
            elif submission_filter == "submission_result_FAIL":
                filter_dict.append(models.Submission.result == "FAIL")
            else:
                pass
        else:
            pass

        if session is not None:
            submissions = (
                db.query(models.Submission)
                .join(models.Assignment)
                .join(models.TrainingSession)
                .filter(models.TrainingSession.id == session)
                .filter(*filter_dict)
                .order_by(*order_dict)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            submissions = (
                db.query(models.Submission)
                .filter(*filter_dict)
                .order_by(*order_dict)
                .offset(skip)
                .limit(limit)
                .all()
            )

        return {"submissions": submissions, "skip": skip, "limit": limit}
    except Exception as e:
        print("Error in getting all submissions. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def show(id: int, db: Session, current_user: schemas_user.User):

    submission_query, submission = get_submission_query(id, db, current_user)

    return submission


def create(
    request: schemas_submission.CreateSubmission,
    db: Session,
    current_user: schemas_user.User,
):
    try:

        new_submission = models.Submission(
            **request.dict(exclude_unset=True),
            submission_date=date.today(),
            user_fk=current_user.id,
        )

        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)
        return new_submission
    except Exception as e:
        print("Error in creating an assignment submission. ", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Somthing went wrong!"
        )


def update_trainee_submission(
    id: int,
    request: schemas_submission.UpdateTraineeSubmission,
    db: Session,
    current_user: schemas_user.User,
):
    submission_query, submission = get_submission_query(id, db, current_user)

    if request.dict(exclude_unset=True):
        submission_query.update(request.dict(exclude_unset=True))

    db.commit()
    db.refresh(submission)

    return submission


def update(id: int, request: schemas_submission.UpdateSubmission, db: Session):
    submission_query, submission = get_submission_query(id, db)

    if "submission_grade" in request.dict(exclude_unset=True):
        assignment = submission.trainee_assignment
        obtained_score, result = get_result(
            assignment, request.submission_grade.dict(exclude_unset=True)
        )

        request.obtained_score = obtained_score
        request.result = result

        if submission.submission_grade:
            data = request.submission_grade.dict(exclude_unset=True)
            db.query(models.Grade).filter(
                models.Grade.related_submission == submission
            ).update(data)
            db.commit()
            db.refresh(submission.submission_grade)
        else:
            grades = models.Grade(
                **request.submission_grade.dict(exclude_unset=True),
                related_submission=submission,
            )
            db.add(grades)
            db.commit()
            db.refresh(grades)
        delattr(request, "submission_grade")

    if request.dict(exclude_unset=True):
        submission_query.update(request.dict(exclude_unset=True))

    db.commit()
    db.refresh(submission)

    return submission


def delete(id: int, db: Session, current_user: schemas_user.User):
    submission_query, submission = get_submission_query(id, db, current_user)

    submission_query.delete()
    db.commit()

    return JSONResponse(
        content={"message": "The assignment submission has been deleted!"}
    )
