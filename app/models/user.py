from sqlalchemy import Column,Integer,String,Boolean,DateTime,Enum
from app.core.database import base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    CFO = "cfo"
    REGIONAL_MANAGER = "regional_manager"
class Users(base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    region = Column(String, nullable=True)
    role = Column(String, nullable=False)