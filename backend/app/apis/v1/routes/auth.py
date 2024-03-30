from datetime import timedelta
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.schemas.token import Token, UserCreate, UserInDB
from app.models.users import User
from internal.config import get_settings, Settings

router = APIRouter(
    prefix='/users',
    tags=['users']
)

def send_new_account_email():
    pass 

def get_user_by_email():
    pass

def create_user():
    pass 

def get_db():
    pass


def create_access_token():
    pass


def authenticate_user():
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

def send_password_reset_email():
    pass

@router.post('/', response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_new_account(user_in: UserCreate, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> Token:
    user = get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail=f"The user with {user_in.email} already exists.",
        )
    new_user: Union[UserInDB, None] = create_user(db, user_in)
    if settings.EMAILS_ENABLED:
        # TODO: Use Anyone method either Email or Password  # pylint: disable=fixme
        await send_new_account_email(email_to=new_user.email, subject="New Account creation email",
                                     html_body="New Account creation body")
    token = create_access_token(subject=new_user.email, expires_delta=timedelta(minutes=1))
    return Token(access_token=token, token_type='bearer')


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
        settings: Settings = Depends(get_settings)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserInDB)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user



@router.post('/forgot-password')
async def send_forgot_password_email(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(detail=f"User with {email} not found", status_code=status.HTTP_401_UNAUTHORIZED)
    await send_password_reset_email(user=user)
    return JSONResponse(content=f"Password Reset Email send successfully to {user.email}",
                        status_code=status.HTTP_200_OK)


@router.post('/reset-password/{token}')
async def reset_user_password(token: str, password: str, db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(detail="Token is required", status_code=status.HTTP_400_BAD_REQUEST)
    user = get_current_user(token=token, db=db)
    if not user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_400_BAD_REQUEST)
    existing_user = db.query(User).filter(User.email == user.email).first()
    existing_user.password = get_password_hash(password.model_dump().get("password"))
    db.commit()
    db.refresh(existing_user)
    return existing_user


@router.post('/login-with-otp')
async def login_with_email_otp(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(detail=f"User with email {email} not found", status_code=status.HTTP_404_NOT_FOUND)
    otp = generate_otp()
    user.otp = otp
    db.commit()
    db.refresh(user)
    await send_email_otp(user=user)
    return JSONResponse(content=f"An otp is send successfully to {user.email}",
                        status_code=status.HTTP_200_OK)


@router.post('/validate-otp')
async def validate_email_otp(email: EmailStr, otp: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(detail=f"User with email {email} not found", status_code=status.HTTP_404_NOT_FOUND)
    if user.otp == otp:
        user.otp = None
        db.commit()
        db.refresh(user)
        token = create_access_token(subject=user.email)
        return Token(access_token=token, token_type='bearer')
    raise HTTPException(detail="Could not validate otp Try again", status_code=status.HTTP_401_UNAUTHORIZED)