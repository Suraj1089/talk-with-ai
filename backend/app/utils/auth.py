from datetime import datetime, timedelta
from typing import Annotated, Any, Union

from app.db.database import engine
from app.internal.config import Settings, get_settings
from app.models.users import User
from app.schemas.token import Token, TokenResponse, UserCreate, UserInDB
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import EmailStr
from sqlmodel import Session, select


def create_access_token(
    settings: Settings,
    subject: Union[str, Any],
    expires_delta: timedelta = None,
) -> tuple[Any, datetime]:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire: datetime = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode: dict = {"exp": expire, "sub": str(subject)}
    encoded_jwt: Any = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt, expire


def create_refresh_token(
    settings: Settings,
    subject: Union[str, Any],
    expires_delta: timedelta = None,
) -> tuple[Any, datetime]:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire: datetime = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode: dict = {"exp": expire, "sub": str(subject)}
    encoded_jwt: Any = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_user(session: Session, username: str) -> Union[User, None]:
    existing_user: Union[User, None] = session.exec(
        select(User).where(User.email == username)
    ).first()
    return existing_user


def authenticate_user(
    session: Session, username: str, password: str
) -> Union[User, None]:
    user: Union[User, None] = get_user(session=session, username=username)
    if user:
        return user
    return None
