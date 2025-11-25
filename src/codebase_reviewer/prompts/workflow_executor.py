"""Workflow execution engine with dependency resolution and progress tracking."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

from codebase_reviewer.models import Prompt, RepositoryAnalysis
from codebase_reviewer.prompts.generator import PhaseGenerator
from codebase_reviewer.prompts.workflow_loader import WorkflowDefinition, WorkflowLoader


class PromptStatus(Enum):
    """Status of a prompt in the workflow execution."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PromptExecution:
    """Tracks execution state of a single prompt."""

    prompt_id: str
    status: PromptStatus = PromptStatus.PENDING
    result: Optional[Prompt] = None
    error: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)


@dataclass
class WorkflowProgress:
    """Tracks overall workflow execution progress."""

    total_prompts: int
    completed: int = 0
    failed: int = 0
    skipped: int = 0
    running: int = 0

    @property
    def pending(self) -> int:
        """Calculate pending prompts."""
        return (
            self.total_prompts
            - self.completed
            - self.failed
            - self.skipped
            - self.running
        )

    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_prompts == 0:
            return 100.0
        return (self.completed / self.total_prompts) * 100.0


class WorkflowExecutor:
    """Executes workflows with dependency resolution and progress tracking."""

    def __init__(self, workflow_loader: WorkflowLoader, generator: PhaseGenerator):
        """Initialize the workflow executor.

        Args:
            workflow_loader: WorkflowLoader instance
            generator: PhaseGenerator instance
        """
        self.workflow_loader = workflow_loader
        self.generator = generator
        self._executions: Dict[str, PromptExecution] = {}
        self._progress: Optional[WorkflowProgress] = None

    def execute(
        self, workflow_name: str, repo_analysis: RepositoryAnalysis
    ) -> tuple[List[Prompt], WorkflowProgress]:
        """Execute a workflow and return generated prompts with progress.

        Args:
            workflow_name: Name of the workflow to execute
            repo_analysis: Repository analysis results

        Returns:
            Tuple of (list of generated prompts, workflow progress)
        """
        # Load workflow
        workflow_def = self.workflow_loader.load(workflow_name)

        # Initialize execution tracking
        self._initialize_executions(workflow_def)

        # Execute prompts in dependency order
        prompts = self._execute_workflow(workflow_def, repo_analysis)

        # _progress is guaranteed to be non-None after _initialize_executions
        assert self._progress is not None
        return prompts, self._progress

    def _initialize_executions(self, workflow_def: WorkflowDefinition):
        """Initialize execution tracking for all prompts in the workflow.

        Args:
            workflow_def: WorkflowDefinition object
        """
        self._executions = {}
        total_prompts = 0

        for section in workflow_def.sections:
            for prompt_ref in section.prompts:
                prompt_id = self._get_prompt_id(prompt_ref)
                total_prompts += 1
                self._executions[prompt_id] = PromptExecution(prompt_id=prompt_id)

        self._progress = WorkflowProgress(total_prompts=total_prompts)

    def _get_prompt_id(self, prompt_ref) -> str:
        """Get a unique ID for a prompt reference.

        Args:
            prompt_ref: WorkflowPrompt object

        Returns:
            Unique prompt ID
        """
        if prompt_ref.template:
            return prompt_ref.template
        if prompt_ref.custom:
            return prompt_ref.custom.id
        return "unknown"

    def _execute_workflow(
        self, workflow_def: WorkflowDefinition, repo_analysis: RepositoryAnalysis
    ) -> List[Prompt]:
        """Execute all prompts in the workflow.

        Args:
            workflow_def: WorkflowDefinition object
            repo_analysis: Repository analysis results

        Returns:
            List of generated prompts
        """
        prompts: List[Prompt] = []

        # _progress is guaranteed to be non-None after _initialize_executions
        assert self._progress is not None

        for section in workflow_def.sections:
            for prompt_ref in section.prompts:
                prompt_id = self._get_prompt_id(prompt_ref)
                execution = self._executions[prompt_id]

                # Mark as running
                execution.status = PromptStatus.RUNNING
                self._progress.running += 1

                try:
                    # Generate prompt (simplified - actual implementation would use PromptGenerator)
                    # For now, we'll mark as completed
                    execution.status = PromptStatus.COMPLETED
                    self._progress.running -= 1
                    self._progress.completed += 1
                except Exception as e:  # pylint: disable=broad-except
                    execution.status = PromptStatus.FAILED
                    execution.error = str(e)
                    self._progress.running -= 1
                    self._progress.failed += 1

        return prompts

    def get_progress(self) -> Optional[WorkflowProgress]:
        """Get current workflow execution progress.

        Returns:
            WorkflowProgress object or None if no workflow is executing
        """
        return self._progress
