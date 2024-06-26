from datetime import datetime
from typing import Optional


from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    first_name: Optional[str] = Field(max_length=40, default="", nullable=True)
    last_name: Optional[str] = Field(max_length=40, default="", nullable=True)
    password: str = Field(min_length=8, nullable=True)
    role: str = Field(max_length=50, nullable=False, default="USER")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now,
    )
    is_active: bool = Field(
        default=True, description="User account status", nullable=True
    )
    is_superuser: bool = Field(default=False, nullable=True)
    otp: bool = Field(
        nullable=True,
        description="To validate user using email or phone one time password",
    )
