"""Loader for v2.0 Phase 1 and Phase 2 prompt templates."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class TaskSchema:
    """Schema definition for a task output."""

    task_id: str
    name: str
    description: str
    output_format: str
    output_schema: Optional[str] = None


@dataclass
class Phase1TemplateV2:
    """Phase 1 prompt template v2.0 structure."""

    version: str
    template_type: str
    security_level: str
    role: str
    context: str
    scan_parameters: Dict[str, str]
    tasks: List[TaskSchema]
    output_requirements: Dict[str, str]
    guidance_spec: Dict[str, List[str]]
    success_criteria: List[str]
    scan_mode_definitions: Dict[str, Dict[str, str]]
    security_notes: str
    execution_notes: str


@dataclass
class Phase2MetaPromptV2:
    """Phase 2 meta-prompt template v2.0 structure."""

    version: str
    template_type: str
    security_level: str
    role: str
    context: str
    obsolescence_detection: Dict[str, Any]
    metrics_tracked: Dict[str, Any]
    learning_capture: Dict[str, str]
    improvements_planning: Dict[str, List[str]]
    regeneration_workflow: Dict[str, Any]
    codebase_context: Dict[str, str]
    user_requirements: Dict[str, str]
    success_criteria: Dict[str, Any]
    quality_standards: Dict[str, Any]
    deliverables: List[str]
    developer_instructions: str
    robustness_guidelines: List[str]
    sample_obsolescence_check: str
    example_learning_entry: str
    example_regeneration_summary: str
    learnings_from_previous_generations: str
    improvements_for_this_generation: str


class PromptTemplateV2Loader:
    """Loader for v2.0 prompt templates."""

    def __init__(self, templates_dir: Optional[Path] = None):
        """Initialize loader.

        Args:
            templates_dir: Directory containing templates (default: prompts/templates/)
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent.parent.parent / "prompts" / "templates"

        self.templates_dir = Path(templates_dir)

    def load_phase1_template(self) -> Phase1TemplateV2:
        """Load Phase 1 prompt template v2.0.

        Returns:
            Phase1TemplateV2 instance

        Raises:
            FileNotFoundError: If template file doesn't exist
            ValueError: If template is invalid
        """
        template_path = self.templates_dir / "phase1-prompt-template.yaml"

        if not template_path.exists():
            raise FileNotFoundError(f"Phase 1 template not found: {template_path}")

        with open(template_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data or "metadata" not in data or "prompt" not in data:
            raise ValueError("Invalid Phase 1 template structure")

        metadata = data["metadata"]
        prompt = data["prompt"]

        # Parse tasks with schemas
        tasks = []
        for task_data in prompt.get("tasks", []):
            tasks.append(
                TaskSchema(
                    task_id=task_data["task_id"],
                    name=task_data["name"],
                    description=task_data["description"],
                    output_format=task_data["output_format"],
                    output_schema=task_data.get("output_schema"),
                )
            )

        return Phase1TemplateV2(
            version=metadata["version"],
            template_type=metadata["template_type"],
            security_level=metadata["security_level"],
            role=prompt["role"],
            context=prompt["context"],
            scan_parameters=prompt["scan_parameters"],
            tasks=tasks,
            output_requirements=data.get("output_requirements", {}),
            guidance_spec=data.get("guidance_spec", {}),
            success_criteria=data.get("success_criteria", []),
            scan_mode_definitions=data.get("scan_mode_definitions", {}),
            security_notes=data.get("security_notes", ""),
            execution_notes=data.get("execution_notes", ""),
        )

    def load_phase2_metaprompt(self) -> Phase2MetaPromptV2:
        """Load Phase 2 meta-prompt template v2.0.

        Returns:
            Phase2MetaPromptV2 instance

        Raises:
            FileNotFoundError: If template file doesn't exist
            ValueError: If template is invalid
        """
        template_path = self.templates_dir / "meta-prompt-template.md"

        if not template_path.exists():
            raise FileNotFoundError(f"Phase 2 meta-prompt not found: {template_path}")

        # Load YAML content
        with open(template_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data or "metadata" not in data or "prompt" not in data:
            raise ValueError("Invalid Phase 2 meta-prompt structure")

        metadata = data["metadata"]
        prompt = data["prompt"]

        return Phase2MetaPromptV2(
            version=metadata["version"],
            template_type=metadata["template_type"],
            security_level=metadata["security_level"],
            role=prompt["role"],
            context=prompt.get("context", ""),
            obsolescence_detection=prompt.get("obsolescence_detection", {}),
            metrics_tracked=prompt.get("metrics_tracked", {}),
            learning_capture=prompt.get("learning_capture", {}),
            improvements_planning=prompt.get("improvements_planning", {}),
            regeneration_workflow=prompt.get("regeneration_workflow", {}),
            codebase_context=prompt.get("codebase_context", {}),
            user_requirements=prompt.get("user_requirements", {}),
            success_criteria=prompt.get("success_criteria", {}),
            quality_standards=prompt.get("quality_standards", {}),
            deliverables=prompt.get("deliverables", []),
            developer_instructions=prompt.get("developer_instructions", ""),
            robustness_guidelines=prompt.get("robustness_guidelines", []),
            sample_obsolescence_check=prompt.get("sample_obsolescence_check", ""),
            example_learning_entry=prompt.get("example_learning_entry", ""),
            example_regeneration_summary=prompt.get("example_regeneration_summary", ""),
            learnings_from_previous_generations=prompt.get("learnings_from_previous_generations", ""),
            improvements_for_this_generation=prompt.get("improvements_for_this_generation", ""),
        )
