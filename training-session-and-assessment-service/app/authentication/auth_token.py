from datetime import datetime, timedelta

import pytz
from app.core.config import settings
from app.schemas import models, schemas_authentication
from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

utc = pytz.UTC


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.HASH_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRY_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.HASH_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, credentials_exception, security_scopes, db: Session):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
        )
        email: str = payload.get("sub")
        user_type: str = payload.get("user_type")
        expiry: int = payload.get("exp")

        token_data = schemas_authentication.TokenData(email=email, expiry=expiry)

        if email is None or user_type is None or expiry is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="token has been expired")
    except (JWTError, ValidationError) as e:
        print(str(e))
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception

    if utc.localize(datetime.utcnow()) > token_data.expiry:
        print("token expire")
        raise credentials_exception

    if security_scopes.scopes == ["all"]:
        security_scopes.scopes = settings.USER_TYPE.split(",")

    if payload.get("user_type") not in security_scopes.scopes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
