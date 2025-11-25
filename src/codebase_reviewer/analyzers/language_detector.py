"""Language and framework detection for code analysis."""

import os
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List

from codebase_reviewer.analyzers.constants import (
    FRAMEWORK_PATTERNS,
    LANGUAGE_EXTENSIONS,
)
from codebase_reviewer.models import EntryPoint, Framework, Language


class LanguageDetector:
    """Detects programming languages and frameworks in a repository."""

    def detect_languages(self, repo_path: str) -> List[Language]:
        """Detect programming languages in repository.

        Args:
            repo_path: Path to repository root

        Returns:
            List of detected languages with percentages
        """
        extension_counts: Counter = Counter()
        extension_lines: Dict[str, int] = {}

        for root, _, files in os.walk(repo_path):
            # Skip common non-source directories
            if any(
                skip in root
                for skip in [
                    ".git",
                    "node_modules",
                    ".venv",
                    "__pycache__",
                    "dist",
                    "build",
                ]
            ):
                continue

            for file in files:
                ext = Path(file).suffix
                if ext:
                    extension_counts[ext] += 1
                    # Count lines for better percentage calculation
                    file_path = Path(root) / file
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            lines = len(f.readlines())
                            extension_lines[ext] = extension_lines.get(ext, 0) + lines
                    except Exception:
                        pass

        # Map extensions to languages
        languages: List[Language] = []
        total_lines = sum(extension_lines.values()) or 1

        for ext, lines in sorted(extension_lines.items(), key=lambda x: x[1], reverse=True):
            if ext in LANGUAGE_EXTENSIONS:
                lang_name = LANGUAGE_EXTENSIONS[ext]
                percentage = (lines / total_lines) * 100
                if percentage >= 1.0:  # Only include languages with >= 1% usage
                    languages.append(
                        Language(
                            name=lang_name,
                            percentage=round(percentage, 2),
                            file_count=extension_counts[ext],
                            line_count=lines,
                        )
                    )

        return languages

    def detect_frameworks(self, repo_path: str) -> List[Framework]:
        """Detect frameworks used in repository.

        Args:
            repo_path: Path to repository root

        Returns:
            List of detected frameworks
        """
        frameworks: List[Framework] = []

        for framework_name, patterns in FRAMEWORK_PATTERNS.items():
            for file_pattern, search_term in patterns:
                if self._search_for_pattern(repo_path, file_pattern, search_term):
                    frameworks.append(Framework(name=framework_name, confidence=0.8))
                    break  # Found this framework, move to next

        return frameworks

    def _search_for_pattern(self, repo_path: str, file_pattern: str, search_term: str) -> bool:
        """Search for pattern in files.

        Args:
            repo_path: Path to repository root
            file_pattern: Glob pattern for files to search
            search_term: Term to search for in files

        Returns:
            True if pattern found, False otherwise
        """
        repo_root = Path(repo_path)

        # Handle exact file matches
        if not any(c in file_pattern for c in ["*", "?"]):
            target_file = repo_root / file_pattern
            if target_file.exists():
                try:
                    content = target_file.read_text(encoding="utf-8", errors="ignore")
                    return search_term.lower() in content.lower()
                except Exception:
                    return False
            return False

        # Handle glob patterns
        for file_path in repo_root.rglob(file_pattern):
            if not self._is_valid_source_path(file_path):
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if search_term.lower() in content.lower():
                    return True
            except Exception:
                continue

        return False

    def find_entry_points(self, repo_path: str, languages: List[Language]) -> List[EntryPoint]:
        """Find application entry points.

        Args:
            repo_path: Path to repository root
            languages: List of detected languages

        Returns:
            List of entry points
        """
        entry_points: List[EntryPoint] = []
        repo_root = Path(repo_path)

        # Common entry point file patterns
        entry_patterns = {
            "main.py": "Python main script",
            "app.py": "Python application",
            "server.py": "Python server",
            "index.js": "JavaScript entry point",
            "server.js": "JavaScript server",
            "main.js": "JavaScript main",
            "Main.java": "Java main class",
            "Program.cs": "C# program",
            "main.go": "Go main",
        }

        for pattern, description in entry_patterns.items():
            for file_path in repo_root.glob(f"**/{pattern}"):
                if self._is_valid_source_path(file_path):
                    entry_points.append(
                        EntryPoint(
                            path=str(file_path.relative_to(repo_root)),
                            entry_type="main",
                            description=description,
                        )
                    )

        return entry_points[:10]  # Limit results

    def _is_valid_source_path(self, path: Path) -> bool:
        """Check if path is in valid source directory."""
        path_str = str(path)
        excluded = [
            ".git",
            "node_modules",
            ".venv",
            "venv",
            "__pycache__",
            "dist",
            "build",
            ".pytest_cache",
            ".mypy_cache",
        ]
        return not any(excl in path_str for excl in excluded)
