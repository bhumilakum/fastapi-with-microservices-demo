from datetime import datetime
from typing import Optional

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
