from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WishlistBase(BaseModel):
    user_id: int


class WishlistCreate(WishlistBase):
    pass


class WishlistUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")


class WishlistRead(WishlistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime