from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.dependencies import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User, Role
from app.schemas.user import UserCreateCFO, UserCreateRM, UserResponse, Token
from app.core.config import settings

router = APIRouter()

@router.post("/register/cfo", response_model=UserResponse)
async def register_cfo(user_in: UserCreateCFO, db: AsyncSession = Depends(get_db)):
    expected_token = settings.COMPANY_SECRETS.get(user_in.company_name)
    if not expected_token or expected_token != user_in.secret_token:
        raise HTTPException(status_code=400, detail="Invalid company secret token.")
    
    result = await db.execute(select(User).filter(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered.")
        
    new_cfo = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        company_name=user_in.company_name,
        role=Role.CFO,
        is_active=True
    )
    db.add(new_cfo)
    await db.commit()
    await db.refresh(new_cfo)
    return new_cfo

@router.post("/register/rm", response_model=UserResponse)
async def register_rm(user_in: UserCreateRM, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered.")
        
    new_rm = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        company_name=user_in.company_name,
        role=Role.RM,
        is_active=False 
    )
    db.add(new_rm)
    await db.commit()
    await db.refresh(new_rm)
    return new_rm

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).filter(
            (User.email == form_data.username) | (User.rm_login_id == form_data.username)
        )
    )
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect login credentials")
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account pending CFO approval.")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}