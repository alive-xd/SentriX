from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class OrganizationBase(BaseModel):
    name: str
    settings: Optional[dict] = Field(default_factory=dict)
    subscription_tier: Optional[str] = "FREE"
    max_users: Optional[int] = 5

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    settings: Optional[dict] = None
    subscription_tier: Optional[str] = None
    max_users: Optional[int] = None

class OrganizationRead(OrganizationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
