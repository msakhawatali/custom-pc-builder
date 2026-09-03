from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    order_id: int
    payment_method: str
    amount: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_id: Optional[str] = None
    status: str
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime