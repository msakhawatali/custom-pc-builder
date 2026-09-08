from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductCompareBase(BaseModel):
    product_id: int


class ProductCompareCreate(ProductCompareBase):
    pass


class ProductCompareUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ProductCompareRead(ProductCompareBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime