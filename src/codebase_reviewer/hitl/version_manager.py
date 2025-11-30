"""Version management for Phase 2 tools."""

import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class VersionMetadata:
    """Metadata for a tool version."""

    version: int
    """Version number (1, 2, 3, ...)."""

    timestamp: str
    """ISO timestamp when version was created."""

    tools_dir: str
    """Path to tools directory."""

    binary_path: Optional[str]
    """Path to compiled binary."""

    status: str
    """Status: active, archived, failed."""

    llm_model: Optional[str] = None
    """LLM model used to generate this version."""

    llm_cost: Optional[float] = None
    """Cost in USD for generation."""

    validation_passed: bool = False
    """Whether validation passed."""

    notes: Optional[str] = None
    """Optional notes about this version."""

    metrics: Optional[Dict] = None
    """Optional metrics for this version."""


class ToolVersionManager:
    """Manages versions of Phase 2 tools."""

    def __init__(self, codebase_path: Path, base_output_dir: Path = Path("/tmp/codebase-reviewer")):
        """Initialize version manager.

        Args:
            codebase_path: Path to the codebase being analyzed
            base_output_dir: Base directory for all outputs
        """
        self.codebase_path = codebase_path
        self.codebase_name = codebase_path.name
        self.base_dir = base_output_dir / self.codebase_name
        self.versions_dir = self.base_dir / "tool-versions"
        self.metadata_file = self.base_dir / "versions.json"

        # Create directories
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.versions_dir.mkdir(parents=True, exist_ok=True)

    def get_next_version(self) -> int:
        """Get the next version number.

        Returns:
            Next version number
        """
        versions = self.list_versions()
        if not versions:
            return 1
        return max(v.version for v in versions) + 1

    def get_active_version(self) -> Optional[VersionMetadata]:
        """Get the currently active version.

        Returns:
            Active version metadata, or None if no active version
        """
        versions = self.list_versions()
        active = [v for v in versions if v.status == "active"]
        if not active:
            return None
        # Return the highest active version
        return max(active, key=lambda v: v.version)

    def register_version(
        self,
        tools_dir: Path,
        binary_path: Optional[Path],
        llm_model: Optional[str] = None,
        llm_cost: Optional[float] = None,
        validation_passed: bool = False,
        notes: Optional[str] = None,
    ) -> VersionMetadata:
        """Register a new version.

        Args:
            tools_dir: Path to tools directory
            binary_path: Path to compiled binary
            llm_model: LLM model used
            llm_cost: Cost in USD
            validation_passed: Whether validation passed
            notes: Optional notes

        Returns:
            Created version metadata
        """
        version = self.get_next_version()
        timestamp = datetime.utcnow().isoformat()

        # Create version-specific directory
        version_dir = self.versions_dir / f"gen{version}"
        version_dir.mkdir(parents=True, exist_ok=True)

        # Copy tools to version directory
        versioned_tools_dir = version_dir / "tools"
        if versioned_tools_dir.exists():
            shutil.rmtree(versioned_tools_dir)
        shutil.copytree(tools_dir, versioned_tools_dir)

        # Copy binary if it exists
        versioned_binary = None
        if binary_path and binary_path.exists():
            versioned_binary = version_dir / "bin" / binary_path.name
            versioned_binary.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(binary_path, versioned_binary)
            versioned_binary.chmod(0o755)

        metadata = VersionMetadata(
            version=version,
            timestamp=timestamp,
            tools_dir=str(versioned_tools_dir),
            binary_path=str(versioned_binary) if versioned_binary else None,
            status="active",
            llm_model=llm_model,
            llm_cost=llm_cost,
            validation_passed=validation_passed,
            notes=notes,
        )

        # Save metadata
        self._save_version_metadata(metadata)

        print(f"✅ Registered version {version}")
        print(f"   Location: {versioned_tools_dir}")
        if versioned_binary:
            print(f"   Binary: {versioned_binary}")

        return metadata

    def list_versions(self) -> List[VersionMetadata]:
        """List all versions.

        Returns:
            List of version metadata, sorted by version number
        """
        if not self.metadata_file.exists():
            return []

        with open(self.metadata_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        versions = [VersionMetadata(**v) for v in data.get("versions", [])]
        return sorted(versions, key=lambda v: v.version)

    def get_version(self, version: int) -> Optional[VersionMetadata]:
        """Get metadata for a specific version.

        Args:
            version: Version number

        Returns:
            Version metadata, or None if not found
        """
        versions = self.list_versions()
        for v in versions:
            if v.version == version:
                return v
        return None

    def set_active_version(self, version: int) -> VersionMetadata:
        """Set a version as active.

        Args:
            version: Version number to activate

        Returns:
            Updated version metadata

        Raises:
            ValueError: If version not found
        """
        versions = self.list_versions()
        target_version = None

        # Deactivate all versions and find target
        for v in versions:
            if v.version == version:
                target_version = v
                v.status = "active"
            elif v.status == "active":
                v.status = "archived"

        if not target_version:
            raise ValueError(f"Version {version} not found")

        # Save updated metadata
        self._save_all_versions(versions)

        print(f"✅ Activated version {version}")
        return target_version

    def archive_version(self, version: int):
        """Archive a version.

        Args:
            version: Version number to archive
        """
        versions = self.list_versions()
        found = False

        for v in versions:
            if v.version == version:
                v.status = "archived"
                found = True
                break

        if not found:
            raise ValueError(f"Version {version} not found")

        self._save_all_versions(versions)
        print(f"📦 Archived version {version}")

    def delete_version(self, version: int):
        """Delete a version permanently.

        Args:
            version: Version number to delete

        Raises:
            ValueError: If trying to delete the active version
        """
        active = self.get_active_version()
        if active and active.version == version:
            raise ValueError(f"Cannot delete active version {version}. Archive it first or activate another version.")

        versions = self.list_versions()
        versions = [v for v in versions if v.version != version]

        # Delete version directory
        version_dir = self.versions_dir / f"gen{version}"
        if version_dir.exists():
            shutil.rmtree(version_dir)

        self._save_all_versions(versions)
        print(f"🗑️  Deleted version {version}")

    def _save_version_metadata(self, metadata: VersionMetadata):
        """Save a single version's metadata."""
        versions = self.list_versions()
        # Replace or append
        versions = [v for v in versions if v.version != metadata.version]
        versions.append(metadata)
        self._save_all_versions(versions)

    def _save_all_versions(self, versions: List[VersionMetadata]):
        """Save all versions to metadata file."""
        data = {"versions": [asdict(v) for v in versions]}
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
