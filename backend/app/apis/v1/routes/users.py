from app.db.database import engine
from app.models.users import User
from app.schemas.users import UserCreate, UserResponse
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session, select


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/all")
def get_users():
    with Session(engine) as session:
        result = session.exec(select(User)).all()
    return result


@router.post("/")
def signup_user(new_user: UserCreate) -> UserResponse:
    with Session(engine) as session:
        existing_user: User | None = session.exec(
            select(User).where(User.email == new_user.email)
        ).first()
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
