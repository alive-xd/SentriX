from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.knowledge import DocCategory

class KnowledgeArticleBase(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    category: DocCategory
    description: str
    content: str
    checklist: List[str] = []
    commands: Optional[List[str]] = []
    contacts: Optional[List[str]] = []
    tags: List[str] = []

class KnowledgeArticleCreate(KnowledgeArticleBase):
    pass

class KnowledgeArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    category: Optional[DocCategory] = None
    description: Optional[str] = None
    content: Optional[str] = None
    checklist: Optional[List[str]] = None
    commands: Optional[List[str]] = None
    contacts: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class KnowledgeArticleRead(KnowledgeArticleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
