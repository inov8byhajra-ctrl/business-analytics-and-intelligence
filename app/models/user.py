from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.core.database import base
import enum

class Role(enum.Enum):
    CFO = "CFO"
    RM = "Regional Manager"

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    company_name = Column(String, nullable=False)
    
    # RM specific fields
    is_active = Column(Boolean, default=True) 
    rm_login_id = Column(String, unique=True, index=True, nullable=True) # 6-digit unique ID