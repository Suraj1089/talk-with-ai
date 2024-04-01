from app.models.users import User

from app.schemas.users import UserCreate
from sqlmodel import Session


def create_user(session: Session, user: UserCreate) -> User:
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
