"""Dependency parsing and analysis."""

import json
import re
from pathlib import Path
from typing import List

from codebase_reviewer.analyzers.constants import DEPENDENCY_FILES
from codebase_reviewer.models import CodeStructure, DependencyInfo


class DependencyParser:
    """Parses and analyzes project dependencies."""

    def analyze_dependencies(self, repo_path: str, structure: CodeStructure) -> List[DependencyInfo]:
        """Analyze project dependencies.

        Args:
            repo_path: Path to repository root
            structure: Code structure information

        Returns:
            List of dependencies
        """
        dependencies: List[DependencyInfo] = []
        repo_root = Path(repo_path)

        # Determine primary language
        primary_lang = structure.languages[0].name if structure.languages else None

        if primary_lang and primary_lang in DEPENDENCY_FILES:
            dep_files = DEPENDENCY_FILES[primary_lang]
            for dep_file in dep_files:
                file_path = repo_root / dep_file
                if file_path.exists():
                    deps = self._parse_dependency_file(file_path, primary_lang)
                    dependencies.extend(deps)

        return dependencies

    def _parse_dependency_file(self, file_path: Path, language: str) -> List[DependencyInfo]:
        """Parse dependency file.

        Args:
            file_path: Path to dependency file
            language: Programming language

        Returns:
            List of dependencies
        """
        dependencies: List[DependencyInfo] = []

        try:
            if file_path.name == "package.json":
                dependencies.extend(self._parse_package_json(file_path))
            elif file_path.name in ["requirements.txt", "requirements-dev.txt"]:
                dependencies.extend(self._parse_requirements_txt(file_path))
            elif file_path.name == "pyproject.toml":
                dependencies.extend(self._parse_pyproject_toml(file_path))
            elif file_path.name == "Cargo.toml":
                dependencies.extend(self._parse_cargo_toml(file_path))
            elif file_path.name == "go.mod":
                dependencies.extend(self._parse_go_mod(file_path))
        except Exception:
            pass

        return dependencies

    def _parse_package_json(self, file_path: Path) -> List[DependencyInfo]:
        """Parse package.json file."""
        dependencies: List[DependencyInfo] = []
        content = json.loads(file_path.read_text(encoding="utf-8"))

        for dep_type in ["dependencies", "devDependencies"]:
            if dep_type in content:
                for name, version in content[dep_type].items():
                    dependencies.append(
                        DependencyInfo(
                            name=name,
                            version=version,
                            dependency_type="dev" if dep_type == "devDependencies" else "runtime",
                            source_file=str(file_path.name),
                        )
                    )

        return dependencies

    def _parse_requirements_txt(self, file_path: Path) -> List[DependencyInfo]:
        """Parse requirements.txt file."""
        dependencies: List[DependencyInfo] = []
        content = file_path.read_text(encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Parse package==version or package>=version
            match = re.match(r"([a-zA-Z0-9_-]+)([>=<~!]+)?([\d.]+)?", line)
            if match:
                name = match.group(1)
                version = match.group(3) if match.group(3) else "latest"
                dependencies.append(
                    DependencyInfo(
                        name=name,
                        version=version,
                        dependency_type="dev" if "dev" in file_path.name else "runtime",
                        source_file=str(file_path.name),
                    )
                )

        return dependencies

    def _parse_pyproject_toml(self, file_path: Path) -> List[DependencyInfo]:
        """Parse pyproject.toml file."""
        dependencies: List[DependencyInfo] = []
        content = file_path.read_text(encoding="utf-8")

        # Simple regex-based parsing (not full TOML parser)
        in_dependencies = False
        for line in content.splitlines():
            line = line.strip()

            if line.startswith("[tool.poetry.dependencies]") or line.startswith("[project.dependencies]"):
                in_dependencies = True
                continue
            elif line.startswith("["):
                in_dependencies = False

            if in_dependencies and "=" in line:
                match = re.match(r'([a-zA-Z0-9_-]+)\s*=\s*["\']([^"\']+)["\']', line)
                if match:
                    name, version = match.groups()
                    if name != "python":
                        dependencies.append(
                            DependencyInfo(name=name, version=version, dependency_type="runtime", source_file=str(file_path.name))
                        )

        return dependencies

    def _parse_cargo_toml(self, file_path: Path) -> List[DependencyInfo]:
        """Parse Cargo.toml file."""
        # Simplified parsing - would need full TOML parser for production
        return []

    def _parse_go_mod(self, file_path: Path) -> List[DependencyInfo]:
        """Parse go.mod file."""
        # Simplified parsing
        return []

