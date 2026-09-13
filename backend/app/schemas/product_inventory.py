from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductInventoryBase(BaseModel):
    product_id: int
    quantity: int = Field(default=0, ge=0)
    reserved_quantity: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=0, ge=0)
    is_in_stock: bool = False


class ProductInventoryCreate(ProductInventoryBase):
    pass


class ProductInventoryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity: Optional[int] = Field(default=None, ge=0)
    reserved_quantity: Optional[int] = Field(default=None, ge=0)
    reorder_level: Optional[int] = Field(default=None, ge=0)
    is_in_stock: Optional[bool] = None


class ProductInventoryRead(ProductInventoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime