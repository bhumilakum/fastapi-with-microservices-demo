from app.authentication import oauth2
from app.authentication.password_hashing import Hash
from app.core import database
from app.schemas import models, schemas
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/create", response_model=schemas.ShowUser)
def create(
    request: schemas.User,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Security(oauth2.get_current_user, scopes=["mentor"]),
):
    new_user = models.User(
        email=request.email,
        password=Hash.bcrypt(request.password),
        user_type=request.user_type,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
