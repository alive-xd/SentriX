from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class Organization(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    settings: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="organization", lazy="selectin")
