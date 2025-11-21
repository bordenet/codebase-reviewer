"""Template loader for prompt configuration files.

This module provides functionality to load and validate prompt templates
from YAML configuration files, decoupling prompt content from code logic.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from codebase_reviewer.models import Prompt


class PromptTemplateError(Exception):
    """Raised when there's an error loading or validating prompt templates."""


class PromptTemplate:
    """Represents a single prompt template loaded from configuration."""

    def __init__(self, template_data: Dict[str, Any]):
        """Initialize a prompt template from dictionary data.

        Args:
            template_data: Dictionary containing template configuration

        Raises:
            PromptTemplateError: If required fields are missing
        """
        self._validate_required_fields(template_data)
        self.id: str = template_data["id"]
        self.title: str = template_data["title"]
        self.objective: str = template_data["objective"]
        self.tasks: List[str] = template_data["tasks"]
        self.deliverable: str = template_data["deliverable"]
        self.ai_model_hints: Dict[str, Any] = template_data.get("ai_model_hints", {})
        self.dependencies: List[str] = template_data.get("dependencies", [])
        self.context_requirements: List[str] = template_data.get("context_requirements", [])
        self.conditional: Optional[str] = template_data.get("conditional")

    def _validate_required_fields(self, data: Dict[str, Any]) -> None:
        """Validate that all required fields are present."""
        required = ["id", "title", "objective", "tasks", "deliverable"]
        missing = [field for field in required if field not in data]
        if missing:
            raise PromptTemplateError(f"Missing required fields: {', '.join(missing)}")

        if not isinstance(data["tasks"], list) or not data["tasks"]:
            raise PromptTemplateError("'tasks' must be a non-empty list")

    def to_prompt(self, context: Dict[str, Any], phase: int) -> Prompt:
        """Convert template to a Prompt instance with provided context.

        Args:
            context: Dictionary of context data to include in the prompt
            phase: Phase number for this prompt

        Returns:
            Prompt instance ready for use
        """
        # Calculate estimated tokens from context
        estimated_tokens = sum(len(str(v)) // 4 for v in context.values())

        return Prompt(
            prompt_id=self.id,
            phase=phase,
            title=self.title,
            context=context,
            objective=self.objective,
            tasks=self.tasks,
            deliverable=self.deliverable,
            ai_model_hints={
                **self.ai_model_hints,
                "estimated_tokens": estimated_tokens,
            },
            dependencies=self.dependencies,
        )


class PromptTemplateLoader:
    """Loads and manages prompt templates from YAML configuration files."""

    def __init__(self, templates_dir: Optional[Path] = None):
        """Initialize the template loader.

        Args:
            templates_dir: Directory containing template YAML files.
                          Defaults to prompts/templates/ in the package.
        """
        if templates_dir is None:
            # Default to templates directory relative to this file
            package_dir = Path(__file__).parent
            templates_dir = package_dir / "templates"

        self.templates_dir = Path(templates_dir)
        self._templates_cache: Dict[int, List[PromptTemplate]] = {}

    def load_phase_templates(self, phase: int) -> List[PromptTemplate]:
        """Load all templates for a specific phase.

        Args:
            phase: Phase number (0-4)

        Returns:
            List of PromptTemplate instances for the phase

        Raises:
            PromptTemplateError: If template file cannot be loaded or is invalid
        """
        # Check cache first
        if phase in self._templates_cache:
            return self._templates_cache[phase]

        template_file = self.templates_dir / f"phase{phase}.yml"

        if not template_file.exists():
            raise PromptTemplateError(
                f"Template file not found: {template_file}. " f"Expected templates in {self.templates_dir}"
            )

        try:
            with open(template_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise PromptTemplateError(f"Invalid YAML in {template_file}: {e}") from e
        except OSError as e:
            raise PromptTemplateError(f"Error reading {template_file}: {e}") from e

        if not isinstance(data, dict) or "prompts" not in data:
            raise PromptTemplateError(
                f"Invalid template structure in {template_file}. " "Expected top-level 'prompts' key."
            )

        templates = []
        for prompt_data in data["prompts"]:
            try:
                templates.append(PromptTemplate(prompt_data))
            except PromptTemplateError as e:
                raise PromptTemplateError(
                    f"Error in template {prompt_data.get('id', 'unknown')} " f"in {template_file}: {e}"
                ) from e

        # Cache the loaded templates
        self._templates_cache[phase] = templates
        return templates

    def get_template(self, phase: int, template_id: str) -> Optional[PromptTemplate]:
        """Get a specific template by phase and ID.

        Args:
            phase: Phase number
            template_id: Template ID (e.g., "0.1")

        Returns:
            PromptTemplate if found, None otherwise
        """
        templates = self.load_phase_templates(phase)
        return next((t for t in templates if t.id == template_id), None)

    def clear_cache(self) -> None:
        """Clear the templates cache. Useful for testing or reloading."""
        self._templates_cache.clear()
