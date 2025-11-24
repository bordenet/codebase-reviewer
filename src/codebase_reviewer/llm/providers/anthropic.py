"""Anthropic (Claude) LLM provider implementation."""

import os
from typing import Optional
import anthropic

from ..client import LLMClient, LLMResponse, LLMError, LLMProvider


class AnthropicProvider(LLMClient):
    """Claude API client implementation."""
    
    # Pricing per 1M tokens (as of 2025-11-24)
    PRICING = {
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    }
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize Anthropic client.
        
        Args:
            api_key: Anthropic API key (or uses ANTHROPIC_API_KEY env var)
            model: Model to use (default: claude-3-5-sonnet-20241022)
        """
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise LLMError(
                "Anthropic API key required. "
                "Set ANTHROPIC_API_KEY env var or pass api_key parameter."
            )
        
        super().__init__(api_key, model)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def get_default_model(self) -> str:
        """Get default Claude model."""
        return "claude-3-5-sonnet-20241022"
    
    def send_prompt(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> LLMResponse:
        """Send prompt to Claude.
        
        Args:
            prompt: The prompt to send
            max_tokens: Max tokens in response (default: 8192)
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional Claude API parameters
            
        Returns:
            LLMResponse with Claude's output
            
        Raises:
            LLMError: If API call fails
        """
        try:
            max_tokens = max_tokens or 8192
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            
            # Extract content
            content = ""
            for block in response.content:
                if hasattr(block, "text"):
                    content += block.text
            
            # Calculate tokens and cost
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            
            cost = self.estimate_cost_detailed(input_tokens, output_tokens)
            
            return LLMResponse(
                content=content,
                provider=LLMProvider.ANTHROPIC,
                model=self.model,
                tokens_used=total_tokens,
                cost_usd=cost,
                metadata={
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "stop_reason": response.stop_reason,
                    "message_id": response.id,
                }
            )
            
        except anthropic.APIError as e:
            raise LLMError(f"Anthropic API error: {e}")
        except Exception as e:
            raise LLMError(f"Unexpected error calling Anthropic: {e}")
    
    def validate_response(self, response: LLMResponse) -> bool:
        """Validate Claude response.
        
        Args:
            response: Response to validate
            
        Returns:
            True if response is complete and valid
        """
        if not response.content:
            return False
        
        # Check if response was truncated
        stop_reason = response.metadata.get("stop_reason")
        if stop_reason == "max_tokens":
            return False  # Response was cut off
        
        # Check for minimum content length
        if len(response.content) < 100:
            return False
        
        return True
    
    def estimate_cost_detailed(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on input and output tokens.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Estimated cost in USD
        """
        pricing = self.PRICING.get(self.model, {"input": 3.00, "output": 15.00})
        
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost
    
    def estimate_cost(self, tokens: int) -> float:
        """Estimate cost for total tokens (assumes 50/50 input/output split).
        
        Args:
            tokens: Total number of tokens
            
        Returns:
            Estimated cost in USD
        """
        return self.estimate_cost_detailed(tokens // 2, tokens // 2)
    
    def get_provider(self) -> LLMProvider:
        """Get provider type."""
        return LLMProvider.ANTHROPIC

