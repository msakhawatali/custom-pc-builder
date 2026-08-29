from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductImageBase(BaseModel):
    product_id: int
    image_url: str
    alt_text: Optional[str] = None
    sort_order: int = 0
    is_primary: bool = False


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageUpdate(BaseModel):
    product_id: Optional[int] = None
    image_url: Optional[str] = None
    alt_text: Optional[str] = None
    sort_order: Optional[int] = None
    is_primary: Optional[bool] = None


class ProductImageRead(ProductImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime