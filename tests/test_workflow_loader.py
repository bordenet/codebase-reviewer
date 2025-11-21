"""Tests for workflow loader."""

from pathlib import Path

import pytest

from codebase_reviewer.prompts.workflow_loader import (
    CustomPrompt,
    WorkflowDefinition,
    WorkflowLoader,
    WorkflowPrompt,
    WorkflowSection,
)


def test_workflow_loader_initialization():
    """Test WorkflowLoader initialization."""
    loader = WorkflowLoader()
    assert loader.workflows_dir.exists()
    assert loader._cache == {}


def test_load_default_workflow():
    """Test loading the default workflow."""
    loader = WorkflowLoader()
    workflow = loader.load("default")

    assert isinstance(workflow, WorkflowDefinition)
    assert workflow.name == "Default Documentation-First Review"
    assert workflow.version == "1.0"
    assert len(workflow.sections) == 5  # 5 phases


def test_load_principal_engineer_workflow():
    """Test loading the principal engineer workflow."""
    loader = WorkflowLoader()
    workflow = loader.load("principal_engineer")

    assert isinstance(workflow, WorkflowDefinition)
    assert workflow.name == "Principal Engineer Strategic Review"
    assert workflow.version == "1.0"
    assert len(workflow.sections) == 6  # 6 sections


def test_workflow_caching():
    """Test that workflows are cached."""
    loader = WorkflowLoader()

    # Load once
    workflow1 = loader.load("default")

    # Load again - should come from cache
    workflow2 = loader.load("default")

    assert workflow1 is workflow2  # Same object


def test_clear_cache():
    """Test cache clearing."""
    loader = WorkflowLoader()

    # Load and cache
    loader.load("default")
    assert "default" in loader._cache

    # Clear cache
    loader.clear_cache()
    assert loader._cache == {}


def test_list_workflows():
    """Test listing available workflows."""
    loader = WorkflowLoader()
    workflows = loader.list_workflows()

    assert isinstance(workflows, list)
    assert "default" in workflows
    assert "principal_engineer" in workflows


def test_load_nonexistent_workflow():
    """Test loading a workflow that doesn't exist."""
    loader = WorkflowLoader()

    with pytest.raises(FileNotFoundError) as exc_info:
        loader.load("nonexistent_workflow")

    assert "Workflow not found" in str(exc_info.value)
    assert "nonexistent_workflow" in str(exc_info.value)


def test_resolve_template_reference():
    """Test resolving template references."""
    loader = WorkflowLoader()

    # With prompt ID
    template_file, prompt_id = loader.resolve_template_reference("phase0.yml#0.1")
    assert template_file == "phase0.yml"
    assert prompt_id == "0.1"

    # Without prompt ID
    template_file, prompt_id = loader.resolve_template_reference("phase1.yml")
    assert template_file == "phase1.yml"
    assert prompt_id is None


def test_get_all_prompt_references():
    """Test getting all prompt references from a workflow."""
    loader = WorkflowLoader()
    workflow = loader.load("default")

    references = loader.get_all_prompt_references(workflow)

    assert isinstance(references, list)
    assert len(references) > 0
    assert "phase0.yml#0.1" in references


def test_workflow_with_custom_prompts():
    """Test workflow with custom prompts."""
    loader = WorkflowLoader()
    workflow = loader.load("principal_engineer")

    # Check that some sections have custom prompts
    has_custom = False
    for section in workflow.sections:
        for prompt in section.prompts:
            if prompt.custom:
                has_custom = True
                assert isinstance(prompt.custom, CustomPrompt)
                assert prompt.custom.id
                assert prompt.custom.title
                assert prompt.custom.prompt

    assert has_custom, "Principal engineer workflow should have custom prompts"


def test_workflow_settings():
    """Test workflow settings."""
    loader = WorkflowLoader()
    workflow = loader.load("default")

    assert workflow.settings is not None
    assert isinstance(workflow.settings.parallel_execution, bool)
    assert isinstance(workflow.settings.fail_fast, bool)
    assert isinstance(workflow.settings.cache_results, bool)


def test_workflow_section_structure():
    """Test workflow section structure."""
    loader = WorkflowLoader()
    workflow = loader.load("default")

    for section in workflow.sections:
        assert isinstance(section, WorkflowSection)
        assert section.id
        assert section.title
        assert isinstance(section.prompts, list)
        assert len(section.prompts) > 0

        for prompt in section.prompts:
            assert isinstance(prompt, WorkflowPrompt)
            # Either template or custom, not both
            assert (prompt.template is not None) != (prompt.custom is not None)
