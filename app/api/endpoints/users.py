from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.dependencies import get_db, get_current_user
from app.models.user import User, Role
import random

router = APIRouter()

@router.post("/approve-rm/{rm_id}")
async def approve_regional_manager(rm_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != Role.CFO:
        raise HTTPException(status_code=403, detail="Not authorized. CFO role required.")
        
    result = await db.execute(select(User).filter(User.id == rm_id, User.role == Role.RM))
    rm_user = result.scalars().first()
    
    if not rm_user:
        raise HTTPException(status_code=404, detail="Regional Manager not found.")
        
    if rm_user.company_name != current_user.company_name:
        raise HTTPException(status_code=403, detail="Cannot approve RM for a different company.")
        
    if rm_user.is_active:
        return {"message": "Regional Manager is already active."}

    while True:
        unique_id = str(random.randint(100000, 999999))
        id_check = await db.execute(select(User).filter(User.rm_login_id == unique_id))
        if not id_check.scalars().first():
            break

    rm_user.is_active = True
    rm_user.rm_login_id = unique_id
    await db.commit()

    return {"message": f"RM approved. Unique ID {unique_id} sent via email."}