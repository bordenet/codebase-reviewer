"""Rollback support for Phase 2 tools."""

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .version_manager import ToolVersionManager, VersionMetadata


@dataclass
class VersionInfo:
    """Information about a version for rollback."""

    version: int
    timestamp: str
    status: str
    validation_passed: bool
    notes: Optional[str] = None


class RollbackManager:
    """Manages rollback operations for Phase 2 tools."""

    def __init__(self, version_manager: ToolVersionManager):
        """Initialize rollback manager.

        Args:
            version_manager: Version manager instance
        """
        self.version_manager = version_manager

    def can_rollback(self) -> bool:
        """Check if rollback is possible.

        Returns:
            True if there are archived versions to rollback to
        """
        versions = self.version_manager.list_versions()
        # Can rollback if there's at least one archived version
        return any(v.status == "archived" for v in versions)

    def list_rollback_targets(self) -> list[VersionInfo]:
        """List available rollback targets.

        Returns:
            List of versions that can be rolled back to
        """
        versions = self.version_manager.list_versions()
        targets = []

        for v in versions:
            if v.status in ["archived", "active"]:
                targets.append(
                    VersionInfo(
                        version=v.version,
                        timestamp=v.timestamp,
                        status=v.status,
                        validation_passed=v.validation_passed,
                        notes=v.notes,
                    )
                )

        return sorted(targets, key=lambda x: x.version, reverse=True)

    def rollback_to_version(self, target_version: int, restore_to_workspace: bool = True) -> VersionMetadata:
        """Rollback to a specific version.

        Args:
            target_version: Version number to rollback to
            restore_to_workspace: Whether to restore files to working directory

        Returns:
            Activated version metadata

        Raises:
            ValueError: If target version not found or invalid
        """
        # Get target version metadata
        target = self.version_manager.get_version(target_version)
        if not target:
            raise ValueError(f"Version {target_version} not found")

        # Verify target has valid tools
        tools_dir = Path(target.tools_dir)
        if not tools_dir.exists():
            raise ValueError(f"Version {target_version} tools directory not found: {tools_dir}")

        print(f"🔄 Rolling back to version {target_version}...")
        print(f"   Timestamp: {target.timestamp}")
        print(f"   Tools: {tools_dir}")

        # Activate the target version
        activated = self.version_manager.set_active_version(target_version)

        # Restore to workspace if requested
        if restore_to_workspace:
            self._restore_to_workspace(activated)

        print(f"✅ Rollback complete!")
        return activated

    def rollback_to_previous(self, restore_to_workspace: bool = True) -> VersionMetadata:
        """Rollback to the previous version.

        Args:
            restore_to_workspace: Whether to restore files to working directory

        Returns:
            Activated version metadata

        Raises:
            ValueError: If no previous version available
        """
        active = self.version_manager.get_active_version()
        if not active:
            raise ValueError("No active version found")

        # Find the previous version
        versions = self.version_manager.list_versions()
        previous_versions = [v for v in versions if v.version < active.version]

        if not previous_versions:
            raise ValueError(f"No previous version to rollback to (current: {active.version})")

        # Get the highest version before current
        previous = max(previous_versions, key=lambda v: v.version)

        return self.rollback_to_version(previous.version, restore_to_workspace)

    def create_rollback_point(self, notes: Optional[str] = None) -> VersionMetadata:
        """Create a rollback point by archiving current active version.

        Args:
            notes: Optional notes for this rollback point

        Returns:
            Archived version metadata

        Raises:
            ValueError: If no active version found
        """
        active = self.version_manager.get_active_version()
        if not active:
            raise ValueError("No active version to create rollback point from")

        # Update notes if provided
        if notes:
            active.notes = notes
            self.version_manager._save_version_metadata(active)

        print(f"📌 Created rollback point: version {active.version}")
        if notes:
            print(f"   Notes: {notes}")

        return active

    def _restore_to_workspace(self, version: VersionMetadata):
        """Restore version files to workspace.

        Args:
            version: Version to restore
        """
        tools_dir = Path(version.tools_dir)
        workspace_dir = self.version_manager.base_dir / f"phase2-tools-gen{version.version}"

        print(f"   Restoring to workspace: {workspace_dir}")

        # Remove existing workspace if it exists
        if workspace_dir.exists():
            shutil.rmtree(workspace_dir)

        # Copy version to workspace
        shutil.copytree(tools_dir, workspace_dir)

        # Copy binary if it exists
        if version.binary_path:
            binary_src = Path(version.binary_path)
            if binary_src.exists():
                binary_dst = workspace_dir / "bin" / binary_src.name
                binary_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(binary_src, binary_dst)
                binary_dst.chmod(0o755)
                print(f"   Binary restored: {binary_dst}")

        print(f"   ✓ Workspace restored")

    def get_rollback_history(self) -> list[tuple[VersionInfo, str]]:
        """Get rollback history with change descriptions.

        Returns:
            List of (version_info, change_description) tuples
        """
        versions = self.version_manager.list_versions()
        history = []

        for i, v in enumerate(sorted(versions, key=lambda x: x.version)):
            version_info = VersionInfo(
                version=v.version,
                timestamp=v.timestamp,
                status=v.status,
                validation_passed=v.validation_passed,
                notes=v.notes,
            )

            # Determine change description
            if i == 0:
                change_desc = "Initial version"
            elif v.notes:
                change_desc = v.notes
            else:
                change_desc = f"Regenerated from version {v.version - 1}"

            history.append((version_info, change_desc))

        return history
