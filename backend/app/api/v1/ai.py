from typing import Any
from fastapi import APIRouter
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/chat", response_model=AIChatResponse)
async def chat(
    *,
    request: AIChatRequest
) -> Any:
    return await ai_service.chat(request)
