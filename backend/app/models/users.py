

from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    first_name: Optional[str] = Field(max_length=40, default="", nullable=True)
    last_name: Optional[str] = Field(max_length=40, default="", nullable=True)
    role: str = Field(max_length=50, nullable=False, default="USER")
