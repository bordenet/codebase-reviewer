"""
Mock LLM for generating context-aware simulation responses.

This package provides realistic LLM-like responses based on the context data
provided to each prompt, enabling effective prompt tuning and evaluation.
"""

from typing import Any

from .generators.architecture import ArchitectureGenerator
from .generators.quality import QualityGenerator
from .generators.readme import ReadmeGenerator
from .generators.security import SecurityGenerator
from .generators.strategy import StrategyGenerator
from .generators.testing import TestingGenerator


class MockLLM:
    """Generates context-aware responses that simulate real LLM behavior."""

    def __init__(self):
        """Initialize the mock LLM with all response generators."""
        self.generators = {
            "readme": ReadmeGenerator(),
            "architecture": ArchitectureGenerator(),
            "quality": QualityGenerator(),
            "security": SecurityGenerator(),
            "testing": TestingGenerator(),
            "strategy": StrategyGenerator(),
        }

        # Map prompt IDs to generators
        self.prompt_routing = {
            "0.1": ("readme", "analyze"),
            "1.1": ("architecture", "validate"),
            "1.2": ("architecture", "analyze_dependencies"),
            "2.1": ("quality", "assess_code"),
            "2.2": ("quality", "review_logging"),
            "3.1": ("testing", "validate_setup"),
            "3.2": ("testing", "review_tests"),
            "static_analysis_summary": ("quality", "static_analysis"),
            "comment_quality": ("quality", "comment_quality"),
            "security.1": ("security", "assess"),
            "security.2": ("security", "error_handling"),
            "arch.1": ("architecture", "call_graph"),
            "arch.2": ("architecture", "git_hotspots"),
            "arch.4": ("architecture", "cohesion_coupling"),
            "strategy.2": ("strategy", "observability"),
            "strategy.3": ("strategy", "testing"),
            "strategy.4": ("strategy", "tech_debt"),
            "strategy.5": ("strategy", "mentorship"),
        }

    def generate_response(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """
        Generate a context-aware response for the given prompt.

        Args:
            prompt_id: Unique identifier for the prompt
            prompt_text: The full prompt text
            context: Context data provided to the prompt
            repository: Repository path being analyzed

        Returns:
            A realistic, context-aware response
        """
        route = self.prompt_routing.get(prompt_id)
        if not route:
            return self._generate_generic_response(prompt_id, prompt_text, context, repository)

        generator_name, method_name = route
        generator = self.generators.get(generator_name)
        if not generator:
            return self._generate_generic_response(prompt_id, prompt_text, context, repository)

        method = getattr(generator, method_name, None)
        if not method:
            return self._generate_generic_response(prompt_id, prompt_text, context, repository)

        return method(prompt_id, prompt_text, context, repository)

    def _generate_generic_response(self, prompt_id: str, prompt_text: str, context: Any, repository: str) -> str:
        """Generate a generic response when no specific generator exists."""
        return f"""# Analysis Response for {prompt_id}

## Summary
Analyzed repository at `{repository}`.

## Context Provided
{self._format_context(context)}

## Findings
Based on the provided context, the analysis is complete.

## Recommendations
1. Review the context data for accuracy
2. Ensure all relevant files are included
3. Validate findings against actual codebase

## Next Steps
- Implement recommended changes
- Re-run analysis to verify improvements
"""

    def _format_context(self, context: Any) -> str:
        """Format context data for display."""
        if isinstance(context, dict):
            items = []
            for key, value in context.items():
                if isinstance(value, (list, dict)):
                    items.append(f"- **{key}**: {len(value)} items")
                else:
                    items.append(f"- **{key}**: {value}")
            return "\n".join(items)
        return str(context)


__all__ = ["MockLLM"]
