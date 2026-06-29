from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ReasoningStep(BaseModel):
    title: str
    status: str
    details: Optional[str] = None

class CodeSnippet(BaseModel):
    label: str
    language: str
    code: str

class AIChatResponse(BaseModel):
    content: str
    reasoningSteps: Optional[List[ReasoningStep]] = None
    codeSnippet: Optional[CodeSnippet] = None

class AIChatRequest(BaseModel):
    query: str
