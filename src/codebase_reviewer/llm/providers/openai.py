"""OpenAI LLM provider implementation."""

import os
from typing import Optional
import openai

from ..client import LLMClient, LLMResponse, LLMError, LLMProvider


class OpenAIProvider(LLMClient):
    """OpenAI API client implementation."""

    # Pricing per 1M tokens (as of 2025-11-24)
    PRICING = {
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize OpenAI client.

        Args:
            api_key: OpenAI API key (or uses OPENAI_API_KEY env var)
            model: Model to use (default: gpt-4-turbo)
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMError(
                "OpenAI API key required. "
                "Set OPENAI_API_KEY env var or pass api_key parameter."
            )

        super().__init__(api_key, model)
        self.client = openai.OpenAI(api_key=api_key)

    def get_default_model(self) -> str:
        """Get default OpenAI model."""
        return "gpt-4-turbo"

    def send_prompt(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs,
    ) -> LLMResponse:
        """Send prompt to OpenAI.

        Args:
            prompt: The prompt to send
            max_tokens: Max tokens in response (default: 4096)
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional OpenAI API parameters

        Returns:
            LLMResponse with OpenAI's output

        Raises:
            LLMError: If API call fails
        """
        try:
            max_tokens = max_tokens or 4096

            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
                **kwargs,
            )

            # Extract content
            content = response.choices[0].message.content or ""

            # Calculate tokens and cost
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens

            cost = self.estimate_cost_detailed(input_tokens, output_tokens)

            return LLMResponse(
                content=content,
                provider=LLMProvider.OPENAI,
                model=self.model,
                tokens_used=total_tokens,
                cost_usd=cost,
                metadata={
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id,
                },
            )

        except openai.APIError as e:
            raise LLMError(f"OpenAI API error: {e}")
        except Exception as e:
            raise LLMError(f"Unexpected error calling OpenAI: {e}")

    def validate_response(self, response: LLMResponse) -> bool:
        """Validate OpenAI response.

        Args:
            response: Response to validate

        Returns:
            True if response is complete and valid
        """
        if not response.content:
            return False

        # Check if response was truncated
        finish_reason = response.metadata.get("finish_reason")
        if finish_reason == "length":
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
        pricing = self.PRICING.get(self.model, {"input": 10.00, "output": 30.00})

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
        return LLMProvider.OPENAI
