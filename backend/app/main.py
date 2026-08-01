from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Custom PC Builder API",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message" : "Custom PC Builder API is running successfully."}