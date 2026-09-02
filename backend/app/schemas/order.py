from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    shipping_full_name: str
    shipping_phone: str
    shipping_address: str
    shipping_city: str
    shipping_state: Optional[str] = None
    shipping_postal_code: Optional[str] = None
    shipping_country: str
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipping_full_name: Optional[str] = None
    shipping_phone: Optional[str] = None
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_postal_code: Optional[str] = None
    shipping_country: Optional[str] = None
    notes: Optional[str] = None


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    order_number: str
    status: str
    payment_status: str
    subtotal: Decimal
    shipping_cost: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime