from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductCompatibilityBase(BaseModel):
    source_category_id: int
    target_category_id: int
    compatibility_key: str
    description: Optional[str] = None
    is_active: bool = True


class ProductCompatibilityCreate(ProductCompatibilityBase):
    pass


class ProductCompatibilityUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_category_id: Optional[int] = None
    target_category_id: Optional[int] = None
    compatibility_key: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ProductCompatibilityRead(ProductCompatibilityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime