from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class ProductSpecificationBase(BaseModel):
    product_id: int
    specifications: dict[str, Any]


class ProductSpecificationCreate(ProductSpecificationBase):
    pass


class ProductSpecificationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    specifications: Optional[dict[str, Any]] = None


class ProductSpecificationRead(ProductSpecificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime