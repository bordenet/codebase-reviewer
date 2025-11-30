"""Tests for Human-in-the-Loop (HITL) features."""

import tempfile
from pathlib import Path

import pytest

from codebase_reviewer.hitl.approval import ApprovalDecision, ApprovalGate, ApprovalRequest
from codebase_reviewer.hitl.rollback import RollbackManager, VersionInfo
from codebase_reviewer.hitl.version_manager import ToolVersionManager, VersionMetadata


class TestVersionManager:
    """Tests for ToolVersionManager."""

    def test_initialize_version_manager(self, tmp_path):
        """Test creating a version manager."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")

        assert vm.codebase_name == "test-codebase"
        assert vm.base_dir.exists()
        assert vm.versions_dir.exists()

    def test_get_next_version(self, tmp_path):
        """Test getting next version number."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")

        # First version should be 1
        assert vm.get_next_version() == 1

    def test_register_version(self, tmp_path):
        """Test registering a new version."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "main.go").write_text("package main")

        binary_path = tmp_path / "binary"
        binary_path.write_text("fake binary")

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        metadata = vm.register_version(
            tools_dir=tools_dir,
            binary_path=binary_path,
            llm_model="test-model",
            llm_cost=0.05,
            validation_passed=True,
            notes="Test version",
        )

        assert metadata.version == 1
        assert metadata.status == "active"
        assert metadata.validation_passed is True
        assert metadata.llm_model == "test-model"
        assert metadata.llm_cost == 0.05
        assert metadata.notes == "Test version"

    def test_list_versions(self, tmp_path):
        """Test listing versions."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "main.go").write_text("package main")

        vm = ToolVersionManager(codebase_path, tmp_path / "output")

        # Register two versions
        vm.register_version(tools_dir, None, notes="Version 1")
        vm.register_version(tools_dir, None, notes="Version 2")

        versions = vm.list_versions()
        assert len(versions) == 2
        assert versions[0].version == 1
        assert versions[1].version == 2

    def test_get_active_version(self, tmp_path):
        """Test getting active version."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        vm.register_version(tools_dir, None)

        active = vm.get_active_version()
        assert active is not None
        assert active.version == 1
        assert active.status == "active"

    def test_set_active_version(self, tmp_path):
        """Test setting a version as active."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")

        # Register two versions
        vm.register_version(tools_dir, None, notes="Version 1")
        vm.register_version(tools_dir, None, notes="Version 2")

        # Version 2 should be active
        active = vm.get_active_version()
        assert active.version == 2

        # Set version 1 as active
        vm.set_active_version(1)
        active = vm.get_active_version()
        assert active.version == 1

    def test_archive_version(self, tmp_path):
        """Test archiving a version."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        vm.register_version(tools_dir, None)

        # Archive version 1
        vm.archive_version(1)

        v = vm.get_version(1)
        assert v.status == "archived"

    def test_delete_version(self, tmp_path):
        """Test deleting a version."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")

        # Register two versions
        vm.register_version(tools_dir, None)
        vm.register_version(tools_dir, None)

        # Delete version 1 (not active)
        vm.set_active_version(2)
        vm.delete_version(1)

        versions = vm.list_versions()
        assert len(versions) == 1
        assert versions[0].version == 2

    def test_cannot_delete_active_version(self, tmp_path):
        """Test that active version cannot be deleted."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        vm.register_version(tools_dir, None)

        # Try to delete active version
        with pytest.raises(ValueError, match="Cannot delete active version"):
            vm.delete_version(1)


class TestRollbackManager:
    """Tests for RollbackManager."""

    def test_can_rollback(self, tmp_path):
        """Test checking if rollback is possible."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        rm = RollbackManager(vm)

        # No versions yet
        assert rm.can_rollback() is False

        # Register one version
        vm.register_version(tools_dir, None)
        # Still can't rollback (only one version)
        assert rm.can_rollback() is False

        # Register second version
        vm.register_version(tools_dir, None)
        # Now we can rollback
        assert rm.can_rollback() is True

    def test_list_rollback_targets(self, tmp_path):
        """Test listing rollback targets."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        rm = RollbackManager(vm)

        # Register versions
        vm.register_version(tools_dir, None, notes="V1")
        vm.register_version(tools_dir, None, notes="V2")

        targets = rm.list_rollback_targets()
        assert len(targets) == 2
        # Should be in reverse order (newest first)
        assert targets[0].version == 2
        assert targets[1].version == 1

    def test_rollback_to_version(self, tmp_path):
        """Test rolling back to a specific version."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "main.go").write_text("package main")

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        rm = RollbackManager(vm)

        # Register two versions
        vm.register_version(tools_dir, None, notes="V1")
        vm.register_version(tools_dir, None, notes="V2")

        # Rollback to version 1
        result = rm.rollback_to_version(1, restore_to_workspace=False)

        assert result.version == 1
        assert vm.get_active_version().version == 1

    def test_rollback_to_previous(self, tmp_path):
        """Test rolling back to previous version."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "main.go").write_text("package main")

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        rm = RollbackManager(vm)

        # Register three versions
        vm.register_version(tools_dir, None, notes="V1")
        vm.register_version(tools_dir, None, notes="V2")
        vm.register_version(tools_dir, None, notes="V3")

        # Active should be 3
        assert vm.get_active_version().version == 3

        # Rollback to previous
        result = rm.rollback_to_previous(restore_to_workspace=False)

        assert result.version == 2
        assert vm.get_active_version().version == 2

    def test_get_rollback_history(self, tmp_path):
        """Test getting rollback history."""
        codebase_path = tmp_path / "test-codebase"
        codebase_path.mkdir()

        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()

        vm = ToolVersionManager(codebase_path, tmp_path / "output")
        rm = RollbackManager(vm)

        vm.register_version(tools_dir, None, notes="First version")
        vm.register_version(tools_dir, None, notes="Second version")

        history = rm.get_rollback_history()
        assert len(history) == 2

        version_info, change_desc = history[0]
        assert version_info.version == 1
        assert change_desc == "Initial version"

        version_info, change_desc = history[1]
        assert version_info.version == 2
        assert change_desc == "Second version"


class TestApprovalGate:
    """Tests for ApprovalGate."""

    def test_auto_approve_low_risk(self):
        """Test auto-approval of low-risk changes."""
        gate = ApprovalGate(auto_approve_low_risk=True)

        request = ApprovalRequest(
            current_version=1,
            proposed_version=2,
            reason="Minor update",
            changes_summary="Small fixes",
            risk_level="low",
            auto_approve=True,
        )

        result = gate.request_approval(request, interactive=False)

        assert result.decision == ApprovalDecision.APPROVED
        assert "Auto-approved" in result.notes

    def test_non_interactive_requires_review(self):
        """Test that non-interactive mode requires review."""
        gate = ApprovalGate(auto_approve_low_risk=False)

        request = ApprovalRequest(
            current_version=1,
            proposed_version=2,
            reason="Update",
            changes_summary="Changes",
            risk_level="medium",
        )

        result = gate.request_approval(request, interactive=False)

        assert result.decision == ApprovalDecision.NEEDS_REVIEW

    def test_format_approval_summary(self):
        """Test formatting approval summary."""
        gate = ApprovalGate()

        request = ApprovalRequest(
            current_version=1,
            proposed_version=2,
            reason="Test update",
            changes_summary="Test changes",
            risk_level="low",
        )

        result = ApprovalDecision.APPROVED
        result_obj = type("Result", (), {"decision": result, "notes": "Test notes", "modifications": None})()

        summary = gate.format_approval_summary(request, result_obj)

        assert "APPROVAL SUMMARY" in summary
        assert "1 → 2" in summary
        assert "Test update" in summary
