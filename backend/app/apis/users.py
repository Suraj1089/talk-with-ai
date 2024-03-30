from sqlmodel import select

from fastapi import APIRouter
from app.models.users import User
from sqlmodel import Session
from app.db.database import engine


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get('/all')
def get_users():
    with Session(engine) as session:
        result = session.exec(select(User)).all()
    return result


@router.post('/signup')
def signup_user() -> dict[str, str]:
    with Session(engine) as session:
        session.add(User(email="suraj1@gmail.com", first_name="suraj", last_name="pisal"))
        session.commit()
    return {"detail": "User created successufully"}
