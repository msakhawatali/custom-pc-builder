from datetime import datetime
from decimal import Decimal
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductVariantBase(BaseModel):
    product_id: int
    name: str
    sku: str
    price: Decimal = Field(gt=0)
    attributes: dict[str, Any]


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0)
    attributes: Optional[dict[str, Any]] = None


class ProductVariantRead(ProductVariantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime