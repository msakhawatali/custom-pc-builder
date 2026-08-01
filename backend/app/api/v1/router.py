from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/v1/health")
def health():
    return {
    "status": "ok",
    "service": "Custom PC Builder API"
    }


# Future feature routers will be included here:
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(products.router, prefix="/products", tags=["products"])