from app.api import api_user
from app.authentication import oauth2
from app.core import database
from app.schemas import enums, schemas_user
from fastapi import APIRouter, BackgroundTasks, Depends, Security, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

"""
    to get the list of all the users and based on usertype
"""


@router.get("/", response_model=schemas_user.ShowUserList)
def get_all(
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
    # user_type: Optional[str] = Query(
    #     None,
    #     description="User type wise filter (admin, mentor, trainee)",
    #     regex=r"^\badmin\b$|^\bmentor\b$|^\btrainee\b$",
    # ),
    user_type: enums.UserTypeEnum = None,
    skip: int = 0,
    limit: int = 50,
):
    return api_user.get_all(db, user_type, skip, limit)


"""
    to get single user profile
"""


@router.get("/{id}", response_model=schemas_user.ShowUser)
def show(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_user.show(id, db)


"""
    to add new user (mentor or trainee)
"""


@router.post(
    "/", response_model=schemas_user.ShowUser, status_code=status.HTTP_201_CREATED
)
def create(
    request: schemas_user.CreateUser,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_user.create(request, db, background_tasks)


"""
    to update user profile
"""


@router.patch(
    "/{id}", response_model=schemas_user.ShowUser, status_code=status.HTTP_202_ACCEPTED
)
def update(
    id: int,
    request: schemas_user.UpdateUser,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin", "mentor"]
    ),
):
    return api_user.update(id, request, db)


"""
    to delete user profile
"""


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas_user.User = Security(
        oauth2.get_current_user, scopes=["admin"]
    ),
):
    return api_user.delete(id, db)
