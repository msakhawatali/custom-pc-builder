from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CouponBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str
    discount_value: Decimal
    minimum_order_amount: Optional[Decimal] = None
    maximum_discount_amount: Optional[Decimal] = None
    usage_limit: Optional[int] = None
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: Optional[str] = None
    description: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[Decimal] = None
    minimum_order_amount: Optional[Decimal] = None
    maximum_discount_amount: Optional[Decimal] = None
    usage_limit: Optional[int] = None
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class CouponRead(CouponBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    used_count: int
    created_at: datetime
    updated_at: datetime