"""Base LLM client interface and response models."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class LLMProvider(Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


@dataclass
class LLMResponse:
    """Response from an LLM provider."""
    
    content: str
    """The main response content."""
    
    provider: LLMProvider
    """Which provider generated this response."""
    
    model: str
    """The specific model used."""
    
    tokens_used: int
    """Total tokens consumed."""
    
    cost_usd: float
    """Estimated cost in USD."""
    
    metadata: Dict[str, Any]
    """Additional provider-specific metadata."""


class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass


class LLMClient(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        """Initialize the LLM client.
        
        Args:
            api_key: API key for the provider
            model: Optional model override (uses provider default if not specified)
        """
        self.api_key = api_key
        self.model = model or self.get_default_model()
    
    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model for this provider."""
        pass
    
    @abstractmethod
    def send_prompt(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Send a prompt to the LLM and get a response.
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response (None = provider default)
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Provider-specific parameters
            
        Returns:
            LLMResponse with the generated content
            
        Raises:
            LLMError: If the request fails
        """
        pass
    
    @abstractmethod
    def validate_response(self, response: LLMResponse) -> bool:
        """Validate that a response is complete and usable.
        
        Args:
            response: The response to validate
            
        Returns:
            True if response is valid, False otherwise
        """
        pass
    
    def estimate_cost(self, tokens: int) -> float:
        """Estimate cost for a given number of tokens.
        
        Args:
            tokens: Number of tokens
            
        Returns:
            Estimated cost in USD
        """
        # Override in subclasses with provider-specific pricing
        return 0.0
    
    def get_provider(self) -> LLMProvider:
        """Get the provider type for this client."""
        # Override in subclasses
        return LLMProvider.ANTHROPIC


def create_client(
    provider: str,
    api_key: str,
    model: Optional[str] = None
) -> LLMClient:
    """Factory function to create an LLM client.
    
    Args:
        provider: Provider name ("anthropic" or "openai")
        api_key: API key for the provider
        model: Optional model override
        
    Returns:
        Configured LLM client
        
    Raises:
        ValueError: If provider is not supported
    """
    from .providers.anthropic import AnthropicProvider
    from .providers.openai import OpenAIProvider
    
    provider_lower = provider.lower()
    
    if provider_lower == "anthropic":
        return AnthropicProvider(api_key, model)
    elif provider_lower == "openai":
        return OpenAIProvider(api_key, model)
    else:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Supported: anthropic, openai"
        )

