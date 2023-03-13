from typing import Any, Dict, List, Optional

from app.schemas.enums import UserTypeEnum
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: str
    user_type: UserTypeEnum
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ShowUser(User):
    id: int

    class Config:
        orm_mode = True


class ShowUserFew(BaseModel):
    id: int
    email: str


class ShowUserList(BaseModel):
    users: List[ShowUser]
    skip: int
    limit: int


class CreateUser(User):
    password: str

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        orm_mode = True


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]
