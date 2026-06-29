from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.schemas.role import RoleRead
from app.schemas.organization import OrganizationRead

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    role: str = "ANALYST"

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(min_length=8)

# Properties to receive via API on update
class UserUpdate(UserBase):
    email: EmailStr | None = None # type: ignore
    password: str | None = Field(default=None, min_length=8)

# Properties to return via API
class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    organization_id: UUID | None = None
    role_id: UUID | None = None
    organization: OrganizationRead | None = None
    role_obj: RoleRead | None = None

    class Config:
        from_attributes = True
