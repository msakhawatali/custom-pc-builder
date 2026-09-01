from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int | None = None


class CartItemRead(CartItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime