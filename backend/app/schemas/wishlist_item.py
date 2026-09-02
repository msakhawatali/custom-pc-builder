from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WishlistItemBase(BaseModel):
    wishlist_id: int
    product_id: int


class WishlistItemCreate(WishlistItemBase):
    pass


class WishlistItemUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")


class WishlistItemRead(WishlistItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime