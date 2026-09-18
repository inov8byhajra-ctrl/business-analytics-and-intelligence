from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    is_active: bool=True
    
class UserCreate(UserBase):
    password:str
    
class UserResponse(UserBase):
    id:int
    is_superuser:bool
    created_at:datetime
    
    
    model_config=ConfigDict(from_attributes=True)
    