from abc import ABC, abstractmethod
from typing import Optional
from models.provider_response import AIResponse

class BaseAIService(ABC):
    """
    Abstract base class for AI service providers
    Standardizes the interface for all AI providers
    """
    
    @abstractmethod
    async def get_completion(self, prompt: str) -> Optional[AIResponse]:
        """
        Get completion from the AI service
        
        Args:
            prompt: The input prompt
            
        Returns:
            AIResponse object with completion details or None on error
        """
        pass
    
    @abstractmethod
    def __init__(self):
        """
        Initialize the service with provider-specific configuration
        """
        pass
        
    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the AI provider
        
        Returns:
            Provider name as string
        """
        pass
        
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the name of the AI model
        
        Returns:
            Model name as string
        """
        pass