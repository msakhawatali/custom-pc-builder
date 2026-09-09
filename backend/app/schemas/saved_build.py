from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class SavedBuildBase(BaseModel):
    name: str
    configuration: dict[str, Any]
    is_active: bool = True


class SavedBuildCreate(SavedBuildBase):
    pass


class SavedBuildUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = None
    configuration: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None


class SavedBuildRead(SavedBuildBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime