from typing import List, Optional

from app.schemas.enums import UserTypeEnum
from pydantic import BaseModel


class User(BaseModel):
    email: str
    user_type: UserTypeEnum
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ShowUser(User):
    id: int

    class Config:
        orm_mode = True


class ShowUserList(BaseModel):
    users: List[ShowUser]
    skip: int
    limit: int


class CreateUser(User):
    password: str

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        orm_mode = True
