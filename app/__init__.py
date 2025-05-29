from fastapi import FastAPI
from app.api.v1.routers import auth_router, users_router

app = FastAPI()

@app.get("/api/v1")
async def root():
    return {"message": "Welcome to the Note App API"}

app.include_router(router=auth_router, prefix="/api/v1")
app.include_router(router=users_router, prefix="/api/v1")