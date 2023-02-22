from datetime import datetime
from typing import Optional

from app.schemas.training_session import (  # noqa
    CreateTrainingSession,
    ShowTrainingSession,
    ShowTrainingSessionList,
    UpdateTrainingSession,
)
from app.schemas.user import (  # noqa
    CreateUser,
    ShowUser,
    ShowUserList,
    UpdateUser,
    User,
)
from pydantic import BaseModel


class JWTToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    expiry: datetime


class Login(BaseModel):
    username: str
    password: str
