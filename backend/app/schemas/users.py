from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    

class UserCreate(UserBase):
    role: Optional[str] = "USER"
    password: str = Field(min_length=8)
    

class UserResponse(UserBase):
    id: int
    