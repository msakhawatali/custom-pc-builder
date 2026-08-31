from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CartBase(BaseModel):
    user_id: int
    is_active: bool = True


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    is_active: bool | None = None


class CartRead(CartBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime