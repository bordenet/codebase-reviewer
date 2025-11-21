"""Tests for workflow executor."""

import pytest

from codebase_reviewer.models import RepositoryAnalysis
from codebase_reviewer.prompts.generator import PhaseGenerator
from codebase_reviewer.prompts.workflow_executor import (
    PromptStatus,
    WorkflowExecutor,
    WorkflowProgress,
)
from codebase_reviewer.prompts.workflow_loader import WorkflowLoader


@pytest.fixture
def workflow_loader():
    """Create a WorkflowLoader instance."""
    return WorkflowLoader()


@pytest.fixture
def generator():
    """Create a PhaseGenerator instance."""
    return PhaseGenerator()


@pytest.fixture
def executor(workflow_loader, generator):
    """Create a WorkflowExecutor instance."""
    return WorkflowExecutor(workflow_loader, generator)


@pytest.fixture
def repo_analysis():
    """Create a minimal RepositoryAnalysis instance."""
    return RepositoryAnalysis(
        repository_path="/test/repo",
        documentation=None,
        code=None,
        validation=None,
    )


def test_workflow_executor_initialization(executor):
    """Test WorkflowExecutor initialization."""
    assert executor.workflow_loader is not None
    assert executor.generator is not None
    assert executor._executions == {}
    assert executor._progress is None


def test_execute_default_workflow(executor, repo_analysis):
    """Test executing the default workflow."""
    prompts, progress = executor.execute("default", repo_analysis)

    assert isinstance(prompts, list)
    assert isinstance(progress, WorkflowProgress)
    assert progress.total_prompts > 0


def test_execute_principal_engineer_workflow(executor, repo_analysis):
    """Test executing the principal engineer workflow."""
    prompts, progress = executor.execute("principal_engineer", repo_analysis)

    assert isinstance(prompts, list)
    assert isinstance(progress, WorkflowProgress)
    assert progress.total_prompts > 0


def test_workflow_progress_tracking(executor, repo_analysis):
    """Test workflow progress tracking."""
    _, progress = executor.execute("default", repo_analysis)

    assert progress.total_prompts > 0
    assert progress.completed >= 0
    assert progress.failed >= 0
    assert progress.skipped >= 0
    assert progress.running == 0  # Should be 0 after execution completes
    assert progress.pending >= 0


def test_workflow_progress_percentage(executor, repo_analysis):
    """Test workflow progress percentage calculation."""
    _, progress = executor.execute("default", repo_analysis)

    assert 0.0 <= progress.completion_percentage <= 100.0


def test_get_progress_before_execution(executor):
    """Test getting progress before any execution."""
    progress = executor.get_progress()
    assert progress is None


def test_get_progress_after_execution(executor, repo_analysis):
    """Test getting progress after execution."""
    executor.execute("default", repo_analysis)
    progress = executor.get_progress()

    assert progress is not None
    assert isinstance(progress, WorkflowProgress)


def test_prompt_status_enum():
    """Test PromptStatus enum values."""
    assert PromptStatus.PENDING.value == "pending"
    assert PromptStatus.RUNNING.value == "running"
    assert PromptStatus.COMPLETED.value == "completed"
    assert PromptStatus.FAILED.value == "failed"
    assert PromptStatus.SKIPPED.value == "skipped"


def test_workflow_progress_pending_calculation():
    """Test WorkflowProgress pending calculation."""
    progress = WorkflowProgress(total_prompts=10, completed=3, failed=1, skipped=1, running=2)

    assert progress.pending == 3  # 10 - 3 - 1 - 1 - 2 = 3


def test_workflow_progress_completion_percentage_zero_total():
    """Test WorkflowProgress completion percentage with zero total."""
    progress = WorkflowProgress(total_prompts=0)

    assert progress.completion_percentage == 100.0


def test_workflow_progress_completion_percentage_partial():
    """Test WorkflowProgress completion percentage with partial completion."""
    progress = WorkflowProgress(total_prompts=10, completed=5)

    assert progress.completion_percentage == 50.0

