from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    CFO = "CFO"
    RM = "Regional Manager"

class UserCreateCFO(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company_name: str
    secret_token: str

class UserCreateRM(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company_name: str

class UserResponse(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    full_name: str
    role: RoleEnum
    company_name: str
    is_active: bool
    rm_login_id: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str