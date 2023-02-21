from typing import List, Union

from app.schemas.enums import UserTypeEnum
from pydantic import BaseModel


class User(BaseModel):
    email: str
    user_type: UserTypeEnum
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None


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
    email: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None

    class Config:
        orm_mode = True
