from fastapi import APIRouter
from app.api.v1.endpoints.product_category import router as product_category_router
from app.api.v1.endpoints.brand import router as brand_router
from app.api.v1.endpoints.supplier import router as supplier_router
from app.api.v1.endpoints.product_image import router as product_image_router
from app.api.v1.endpoints.product_review import router as product_review_router
from app.api.v1.endpoints.product import router as product_router
from app.api.v1.endpoints.product_specification import router as product_specification_router
from app.api.v1.endpoints.product_compatibility import router as product_compatibility_router
from app.api.v1.endpoints.product_inventory import router as product_inventory_router
from app.api.v1.endpoints.product_variant import router as product_variant_router
from app.api.v1.endpoints.customer_address import router as customer_address_router
from app.api.v1.endpoints.cart import router as cart_router
from app.api.v1.endpoints.cart_item import router as cart_item_router
from app.api.v1.endpoints.wishlist import router as wishlist_router
from app.api.v1.endpoints.wishlist_item import router as wishlist_item_router
from app.api.v1.endpoints.order import router as order_router
from app.api.v1.endpoints.order_item import router as order_item_router
from app.api.v1.endpoints.payment import router as payment_router
from app.api.coupons import router as coupon_router








api_router = APIRouter()

@api_router.get("/health")
def health():
    return {"status": "ok", "service": "Custom PC Builder API"}

api_router.include_router(product_category_router)
api_router.include_router(brand_router)
api_router.include_router(supplier_router)
api_router.include_router(product_image_router)
api_router.include_router(product_review_router)
api_router.include_router(product_router)
api_router.include_router(product_specification_router)
api_router.include_router(product_compatibility_router)
api_router.include_router(product_inventory_router)
api_router.include_router(product_variant_router)
api_router.include_router(customer_address_router)
api_router.include_router(cart_router)
api_router.include_router(cart_item_router)
api_router.include_router(wishlist_router)
api_router.include_router(wishlist_item_router)
api_router.include_router(order_router)
api_router.include_router(order_item_router)
api_router.include_router(payment_router)
api_router.include_router(coupon_router)