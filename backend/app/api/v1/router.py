from fastapi import APIRouter
from app.api.v1.endpoints.product_category import router as product_category_router
from app.api.v1.endpoints.brand import router as brand_router
from app.api.v1.endpoints.supplier import router as supplier_router



api_router = APIRouter()

@api_router.get("/health")
def health():
    return {"status": "ok", "service": "Custom PC Builder API"}

api_router.include_router(product_category_router)
api_router.include_router(brand_router)
api_router.include_router(supplier_router)