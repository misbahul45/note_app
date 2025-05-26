from fastapi import FastAPI
import app.api.v1.routers.auth_router as auth_router_module

app=FastAPI()

@app.get("/api/v1")
async def root():
    return {"message": "Welcome to the Note App API"}
app.include_router(router=auth_router_module.auth_router, prefix="/api/v1")