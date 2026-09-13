from app.schemas.product import ProductBase, ProductCreate, ProductUpdate, ProductRead
from app.schemas.brand import BrandBase, BrandCreate, BrandUpdate, BrandRead
from app.schemas.supplier import SupplierBase, SupplierCreate, SupplierUpdate, SupplierRead
from app.schemas.product_image import ProductImageBase, ProductImageCreate, ProductImageUpdate, ProductImageRead
from app.schemas.product_review import ProductReviewBase, ProductReviewCreate, ProductReviewUpdate, ProductReviewRead
from app.schemas.cart import CartBase, CartCreate, CartUpdate, CartRead
from app.schemas.cart_item import CartItemBase, CartItemCreate, CartItemUpdate, CartItemRead
from app.schemas.wishlist import WishlistBase, WishlistCreate, WishlistUpdate, WishlistRead
from app.schemas.order import OrderBase, OrderCreate, OrderUpdate, OrderRead
from app.schemas.order_item import OrderItemBase, OrderItemCreate, OrderItemUpdate, OrderItemRead
from app.schemas.payment import PaymentBase, PaymentCreate, PaymentUpdate, PaymentRead
from app.schemas.coupon import CouponBase, CouponCreate, CouponUpdate, CouponRead
from app.schemas.coupon_usage import CouponUsageBase, CouponUsageCreate, CouponUsageUpdate, CouponUsageRead
from app.schemas.saved_build import SavedBuildBase, SavedBuildCreate, SavedBuildUpdate, SavedBuildRead

from app.schemas.product_compare import (
    ProductCompareBase,
    ProductCompareCreate,
    ProductCompareUpdate,
    ProductCompareRead,
)
from app.schemas.product_category import (
    ProductCategoryBase,
    ProductCategoryCreate,
    ProductCategoryUpdate,
    ProductCategoryRead,
)
from app.schemas.customer_address import (
    CustomerAddressBase,
    CustomerAddressCreate,
    CustomerAddressUpdate,
    CustomerAddressRead,
)
from app.schemas.wishlist_item import (
    WishlistItemBase,
    WishlistItemCreate,
    WishlistItemUpdate,
    WishlistItemRead,
)
from app.schemas.saved_build_item import (
    SavedBuildItemBase,
    SavedBuildItemCreate,
    SavedBuildItemUpdate,
    SavedBuildItemRead,
)
from app.schemas.product_specification import (
    ProductSpecificationBase,
    ProductSpecificationCreate,
    ProductSpecificationUpdate,
    ProductSpecificationRead,
)
from app.schemas.product_compatibility import (
    ProductCompatibilityBase,
    ProductCompatibilityCreate,
    ProductCompatibilityUpdate,
    ProductCompatibilityRead,
)
from app.schemas.product_inventory import (
    ProductInventoryBase,
    ProductInventoryCreate,
    ProductInventoryUpdate,
    ProductInventoryRead,
)
from app.schemas.product_variant import (
    ProductVariantBase,
    ProductVariantCreate,
    ProductVariantUpdate,
    ProductVariantRead,
)

__all__ = ["ProductBase", "ProductCreate", "ProductUpdate", "ProductRead", "ProductCategoryBase", "ProductCategoryCreate", "ProductCategoryUpdate", "ProductCategoryRead", "BrandBase", "BrandCreate", "BrandUpdate", "BrandRead", "SupplierBase", "SupplierCreate", "SupplierUpdate", "SupplierRead",  "ProductImageBase", "ProductImageCreate", "ProductImageUpdate", "ProductImageRead", "ProductReviewBase", "ProductReviewCreate", "ProductReviewUpdate", "ProductReviewRead", "CustomerAddressBase", "CustomerAddressCreate", "CustomerAddressUpdate", "CustomerAddressRead", "CartBase", "CartCreate", "CartUpdate", "CartRead", "CartItemBase", "CartItemCreate", "CartItemUpdate", "CartItemRead", "WishlistBase", "WishlistCreate", "WishlistUpdate", "WishlistRead", "WishlistItemBase", "WishlistItemCreate", "WishlistItemUpdate", "WishlistItemRead", "OrderBase", "OrderCreate", "OrderUpdate", "OrderRead", "OrderItemBase", "OrderItemCreate", "OrderItemUpdate", "OrderItemRead", "PaymentBase", "PaymentCreate", "PaymentUpdate", "PaymentRead", "CouponBase", "CouponCreate", "CouponUpdate", "CouponRead","CouponUsageBase", "CouponUsageCreate", "CouponUsageUpdate", "CouponUsageRead", "ProductCompareBase", "ProductCompareCreate", "ProductCompareUpdate", "ProductCompareRead", "SavedBuildBase", "SavedBuildCreate", "SavedBuildUpdate", "SavedBuildRead", "SavedBuildItemBase", "SavedBuildItemCreate", "SavedBuildItemUpdate", "SavedBuildItemRead", "ProductSpecificationBase", "ProductSpecificationCreate", "ProductSpecificationUpdate", "ProductSpecificationRead", "ProductCompatibilityBase", "ProductCompatibilityCreate", "ProductCompatibilityUpdate", "ProductCompatibilityRead", "ProductInventoryBase", "ProductInventoryCreate", "ProductInventoryUpdate", "ProductInventoryRead", "ProductVariantBase", "ProductVariantCreate", "ProductVariantUpdate", "ProductVariantRead",]