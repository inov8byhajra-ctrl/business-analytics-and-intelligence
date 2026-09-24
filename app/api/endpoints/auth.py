from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.dependencies import get_db
from app.models.user import Users
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check karein ke email pehle se register toh nahi hai
    result = await db.execute(select(Users).where(Users.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Yeh email pehle se registered hai!"
        )
    
    # 2. Password ko hash karein
    hashed_password = get_password_hash(user_in.password)
    
    # 3. Naya user object banayein (apne model ke mutabiq)
    new_user = Users(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role if hasattr(user_in, 'role') else "regional_manager",
        region=user_in.region if hasattr(user_in, 'region') else None
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User kamyabi ke sath register ho gaya hai!", "email": new_user.email}


@router.post("/login")
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    # 1. User ko database mein dhoondein
    result = await db.execute(select(Users).where(Users.email == user_in.email))
    user = result.scalars().first()
    
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ghalat email ya password!"
        )
    
    # 2. JWT token generate karein jisme role bhi shamil ho
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    
    return {"access_token": access_token, "token_type": "bearer"}