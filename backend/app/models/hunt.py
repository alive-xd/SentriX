from typing import Optional
from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class SavedHunt(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "saved_hunts"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="General")
    starred: Mapped[bool] = mapped_column(Boolean, default=False)
    last_run: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
