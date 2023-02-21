from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.enums import UserTypeEnum
from typing import List, Union

from app.schemas.user import (
    User,
    ShowUser,
    ShowUserList,
    CreateUser,
    UpdateUser
)

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
