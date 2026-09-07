from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class CouponUsageBase(BaseModel):
    coupon_id: int
    order_id: int
    discount_amount: Decimal


class CouponUsageCreate(CouponUsageBase):
    pass


class CouponUsageUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CouponUsageRead(CouponUsageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime