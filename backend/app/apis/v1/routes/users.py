
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


@router.post("/signup")
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



# @router.put("/{user_id}", response_model=schemas.User)
# def update_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_id: UUID4,
#     user_in: schemas.UserUpdate,
#     current_user: models.User = Security(
#         deps.get_current_active_user,
#         scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
#     ),
# ) -> Any:
#     """
#     Update a user.
#     """
#     user = crud.user.get(db, id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system",
#         )
#     user = crud.user.update(db, db_obj=user, obj_in=user_in)
#     return user


# @router.get("/me", response_model=schemas.User)
# def read_user_me(
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get current user.
#     """
#     if not current_user.user_role:
#         role = None
#     else:
#         role = current_user.user_role.role.name
#     user_data = schemas.User(
#         id=current_user.id,
#         email=current_user.email,
#         is_active=current_user.is_active,
#         full_name=current_user.full_name,
#         created_at=current_user.created_at,
#         updated_at=current_user.updated_at,
#         role=role,
#     )
#     return user_data


# @router.put("/me", response_model=schemas.User)
# def update_user_me(
    # # *,
    # db: Session = Depends(deps.get_db),
    # full_name: str = Body(None),
    # phone_number: str = Body(None),
    # email: EmailStr = Body(None),
    # current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
    # """
    # Update own user.
    # """
    # current_user_data = jsonable_encoder(current_user)
    # user_in = schemas.UserUpdate(**current_user_data)
    # if phone_number is not None:
    #     user_in.phone_number = phone_number
    # if full_name is not None:
    #     user_in.full_name = full_name
    # if email is not None:
    #     user_in.email = email
    # user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    # return user