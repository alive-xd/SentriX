import enum
import uuid
from typing import Optional, List
from sqlalchemy import String, Text, Enum as SAEnum, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class DocCategory(str, enum.Enum):
    SOP = 'SOP'
    IR = 'IR'
    Intel = 'Intel'
    Admin = 'Admin'
    General = 'General'

class KnowledgeArticle(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'knowledge_articles'

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[DocCategory] = mapped_column(SAEnum(DocCategory, name='doccategory'), nullable=False, default=DocCategory.SOP)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    checklist: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False, default=[])
    commands: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    contacts: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    tags: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False, default=[])
