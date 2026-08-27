from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BrandBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    is_active: bool = True


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    is_active: Optional[bool] = None


class BrandRead(BrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime