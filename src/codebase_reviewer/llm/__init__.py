"""LLM Integration Layer for Phase 2 Tool Generation.

This module provides integration with LLM providers (Claude, OpenAI) to:
1. Send Phase 1 prompts to LLMs
2. Parse LLM responses
3. Extract code blocks from responses
4. Validate response completeness
"""

from .client import LLMClient, LLMResponse, LLMError
from .providers.anthropic import AnthropicProvider
from .providers.openai import OpenAIProvider
from .code_extractor import CodeExtractor

__all__ = [
    "LLMClient",
    "LLMResponse",
    "LLMError",
    "AnthropicProvider",
    "OpenAIProvider",
    "CodeExtractor",
]

