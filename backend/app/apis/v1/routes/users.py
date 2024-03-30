
from app.db.database import engine
from app.models.users import User
from app.schemas.users import UserCreate, UserResponse
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.schemas.token import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import Depends
from fastapi import HTTPException, status

from backend.app.internal.config import Settings, get_settings

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/all")
def get_users():
    with Session(engine) as session:
        result = session.exec(select(User)).all()
    return result


@router.post("/")
def signup_user(new_user: UserCreate) -> UserResponse:
    with Session(engine) as session:
        existing_user: User | None = session.exec(select(User).where(User.email == new_user.email)).first()
        if existing_user:
            return JSONResponse(content="User Already exist", status_code=401)
        user = User(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email,
            password=new_user.last_name,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    
def authenticate_user():
    return {}

def create_access_token():
    return {}

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        settings: Settings = Depends(get_settings)
):
    user = authenticate_user(form_data.username, form_data.password)
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