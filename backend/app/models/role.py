from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User
from app.db.base_class import Base, UUIDMixin, TimestampMixin

class Role(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    permissions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    users: Mapped[List["User"]] = relationship("User", back_populates="role_obj", lazy="selectin")
