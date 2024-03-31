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
from app.utils.auth import create_access_token,create_refresh_token, get_user, authenticate_user
from app.utils.email_utils import send_email, send_email_otp, send_new_account_email, send_password_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])



def get_user_by_email():
    pass


def get_db():
    pass




def generate_otp():
    pass


def send_email_otp():
    pass


def get_current_active_user():
    pass


def get_password_hash():
    pass


def get_current_user():
    pass



def create_user(session: Session, user: UserCreate):
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.last_name,
    )
    session.add(instance=new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup_user(user: UserCreate, settings: Settings = Depends(get_settings)):
    with Session(engine) as session:
        existing_user: User | None = get_user(session=session, username=user.email)
        if existing_user:
            return JSONResponse(content="User Already exist", status_code=401)
        new_user: User = create_user(session=session, user=user)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expire = create_access_token(
            settings, new_user.email, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            settings, user.email, expires_delta=access_token_expires
        )
        if settings.EMAILS_ENABLED:
            await send_new_account_email(email_to=new_user.email, subject="New Account creation email",
                                     html_body="New Account created succefully")
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expiry=expire,
        )


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    with Session(engine) as session:
        user: User | None = authenticate_user(
            session, form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        print(
            access_token_expires,
            settings.ALGORITHM2,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        access_token, expire = create_access_token(
            settings, user.email, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            settings, user.email, expires_delta=access_token_expires
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expiry=expire,
        )


@router.get("/me", response_model=UserInDB)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.post("/forgot-password")
async def send_forgot_password_email(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            detail=f"User with {email} not found",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    await send_password_reset_email(user=user)
    return JSONResponse(
        content=f"Password Reset Email send successfully to {user.email}",
        status_code=status.HTTP_200_OK,
    )


@router.post("/reset-password/{token}")
async def reset_user_password(token: str, password: str, db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(
            detail="Token is required", status_code=status.HTTP_400_BAD_REQUEST
        )
    user = get_current_user(token=token, db=db)
    if not user:
        raise HTTPException(
            detail="User not found", status_code=status.HTTP_400_BAD_REQUEST
        )
    existing_user = db.query(User).filter(User.email == user.email).first()
    existing_user.password = get_password_hash(password.model_dump().get("password"))
    db.commit()
    db.refresh(existing_user)
    return existing_user


@router.post("/login-with-otp")
async def login_with_email_otp(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            detail=f"User with email {email} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    otp = generate_otp()
    user.otp = otp
    db.commit()
    db.refresh(user)
    await send_email_otp(user=user)
    return JSONResponse(
        content=f"An otp is send successfully to {user.email}",
        status_code=status.HTTP_200_OK,
    )


@router.post("/validate-otp")
async def validate_email_otp(email: EmailStr, otp: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            detail=f"User with email {email} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if user.otp == otp:
        user.otp = None
        db.commit()
        db.refresh(user)
        token = create_access_token(subject=user.email)
        return Token(access_token=token, token_type="bearer")
    raise HTTPException(
        detail="Could not validate otp Try again",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
