from typing import Optional

from pydantic import BaseModel


class JWTToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class User(BaseModel):
    email: str
    password: str
    user_type: str


class ShowUser(BaseModel):
    email: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str
