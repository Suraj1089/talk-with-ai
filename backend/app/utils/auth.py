from datetime import datetime, timedelta
from typing import Any, Union

from app.internal.config import Settings
from app.models.users import User
from jose import jwt
from sqlmodel import Session, select
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
