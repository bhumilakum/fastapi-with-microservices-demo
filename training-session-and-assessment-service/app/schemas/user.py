from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.enums import UserTypeEnum
from typing import List, Union


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
