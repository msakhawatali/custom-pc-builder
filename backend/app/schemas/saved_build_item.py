from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SavedBuildItemBase(BaseModel):
    saved_build_id: int
    product_id: int
    quantity: int = Field(default=1, ge=1)


class SavedBuildItemCreate(SavedBuildItemBase):
    pass


class SavedBuildItemUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity: Optional[int] = Field(default=None, ge=1)


class SavedBuildItemRead(SavedBuildItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime