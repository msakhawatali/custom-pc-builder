from fastapi import FastAPI

app = FastAPI(
    title="Custom PC Builder API",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message" : "Custom PC Builder API is running successfully."}