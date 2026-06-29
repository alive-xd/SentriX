from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

class BaseLLMAdapter(ABC):
    """
    Abstract base class for all LLM providers (OpenAI, Claude, Gemini, etc.).
    Provides a consistent interface for the agents to use.
    """
    
    @abstractmethod
    async def generate_response(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        temperature: float = 0.2
    ) -> str:
        """Generate a standard text response."""
        pass
        
    @abstractmethod
    async def generate_structured_response(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        response_model: Type[BaseModel],
        temperature: float = 0.2
    ) -> BaseModel:
        """Generate a structured response adhering to a Pydantic schema."""
        pass
