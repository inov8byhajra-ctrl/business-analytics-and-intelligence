from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.models.user import Users

from app.core.database import engine,base 
from app.api.endpoints import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"starting {settings.PROJECT_NAME}.... ")
    
    async with engine.begin() as conn:
        
        await conn.run_sync(base.metadata.create_all)
    print("database tables created successfully.")
    
    yield
    print("server is shutting down ...")
    
    await engine.dispose()
    print("database connecion closed")


app = FastAPI(title=settings.PROJECT_NAME,lifespan=lifespan)

@app.get("/")
async def home():
    return {"project":settings.PROJECT_NAME,"status":"online"}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])