from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductReviewBase(BaseModel):
    product_id: int
    user_id: int
    rating: int = Field(ge=1, le=5)
    title: Optional[str] = None
    comment: Optional[str] = None


class ProductReviewCreate(ProductReviewBase):
    pass


class ProductReviewUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    title: Optional[str] = None
    comment: Optional[str] = None


class ProductReviewRead(ProductReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime