"""Workflow configuration loader and validator."""

from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
from pydantic import BaseModel, Field, field_validator


class CustomPrompt(BaseModel):
    """Custom prompt definition."""

    id: str
    title: str
    prompt: str
    objective: Optional[str] = None
    tasks: Optional[List[str]] = None
    deliverable: Optional[str] = None


class WorkflowPrompt(BaseModel):
    """A single prompt reference in a workflow."""

    template: Optional[str] = None  # e.g., "phase0.yml#0.1"
    custom: Optional[CustomPrompt] = None


class WorkflowSection(BaseModel):
    """A section (accordion) in a workflow."""

    id: str
    title: str
    description: Optional[str] = None
    prompts: List[WorkflowPrompt]


class WorkflowSettings(BaseModel):
    """Global workflow settings."""

    parallel_execution: bool = False
    fail_fast: bool = False
    cache_results: bool = True


class WorkflowDefinition(BaseModel):
    """Complete workflow definition."""

    name: str
    version: str
    description: str
    settings: WorkflowSettings = Field(default_factory=WorkflowSettings)
    sections: List[WorkflowSection]


class WorkflowLoader:
    """Loads and validates workflow YAML files."""

    def __init__(self, workflows_dir: Optional[Path] = None):
        """Initialize with workflows directory.

        Args:
            workflows_dir: Directory containing workflow YAML files.
                          Defaults to src/codebase_reviewer/prompts/workflows/
        """
        if workflows_dir is None:
            workflows_dir = Path(__file__).parent / "workflows"
        self.workflows_dir = Path(workflows_dir)
        self._cache: Dict[str, WorkflowDefinition] = {}

    def load(self, workflow_name: str) -> WorkflowDefinition:
        """Load a workflow by name.

        Args:
            workflow_name: Name of the workflow (without .yml extension)

        Returns:
            WorkflowDefinition object

        Raises:
            FileNotFoundError: If workflow file doesn't exist
            ValueError: If workflow YAML is invalid
        """
        if workflow_name in self._cache:
            return self._cache[workflow_name]

        workflow_path = self.workflows_dir / f"{workflow_name}.yml"
        if not workflow_path.exists():
            raise FileNotFoundError(
                f"Workflow not found: {workflow_name}\n"
                f"Searched in: {self.workflows_dir}\n"
                f"Available workflows: {', '.join(self.list_workflows())}"
            )

        with open(workflow_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if "workflow" not in data:
            raise ValueError(f"Invalid workflow file: {workflow_path}. Missing 'workflow' key.")

        workflow = WorkflowDefinition(**data["workflow"])
        self._cache[workflow_name] = workflow
        return workflow

    def list_workflows(self) -> List[str]:
        """List all available workflows.

        Returns:
            List of workflow names (without .yml extension)
        """
        if not self.workflows_dir.exists():
            return []
        return [p.stem for p in self.workflows_dir.glob("*.yml")]

    def clear_cache(self):
        """Clear the workflow cache."""
        self._cache.clear()

    def resolve_template_reference(self, template_ref: str) -> tuple[str, Optional[str]]:
        """Resolve a template reference like 'phase0.yml#0.1'.

        Args:
            template_ref: Template reference string

        Returns:
            Tuple of (template_file, prompt_id)
        """
        if "#" in template_ref:
            template_file, prompt_id = template_ref.split("#", 1)
            return template_file, prompt_id
        return template_ref, None

    def get_all_prompt_references(self, workflow: WorkflowDefinition) -> List[str]:
        """Get all template references used in a workflow.

        Args:
            workflow: WorkflowDefinition object

        Returns:
            List of template references (e.g., ['phase0.yml#0.1', 'phase1.yml#1.1'])
        """
        references = []
        for section in workflow.sections:
            for prompt in section.prompts:
                if prompt.template:
                    references.append(prompt.template)
        return references

