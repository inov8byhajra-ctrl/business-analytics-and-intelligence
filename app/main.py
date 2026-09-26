from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import auth, users
from app.core.database import engine, base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs asynchronously when the server starts
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
    yield
    # Code here would run on server shutdown if needed

app = FastAPI(title="InsightFlow Business Analytics API", lifespan=lifespan)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users & RBAC"])

@app.get("/")
def root():
    return {"message": "InsightFlow API is running"}