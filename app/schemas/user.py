from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    is_active: bool=True
    
class UserCreate(UserBase):
    password:str 
    role: str = "regional_manager"
    region: str | None = None
    
class UserResponse(UserBase):
    id:int
    is_superuser:bool
    created_at:datetime
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    model_config=ConfigDict(from_attributes=True)
    