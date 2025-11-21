"""Code quality checking and issue detection."""

import os
import re
from pathlib import Path
from typing import List

from codebase_reviewer.models import Issue, Severity


class QualityChecker:
    """Performs code quality checks and detects common issues."""

    def analyze_quality(self, repo_path: str) -> List[Issue]:
        """Perform basic code quality analysis.

        Args:
            repo_path: Path to repository root

        Returns:
            List of quality issues
        """
        issues: List[Issue] = []

        # Check for TODOs/FIXMEs
        issues.extend(self._check_for_todos(repo_path))

        # Check for basic security issues
        issues.extend(self._check_for_security_issues(repo_path))

        return issues

    def _check_for_todos(self, repo_path: str) -> List[Issue]:
        """Find TODO/FIXME/HACK comments.

        Args:
            repo_path: Path to repository root

        Returns:
            List of TODO/FIXME issues
        """
        issues: List[Issue] = []
        todo_pattern = re.compile(r"#\s*(TODO|FIXME|HACK|XXX):\s*(.+)", re.IGNORECASE)

        for root, _, files in os.walk(repo_path):
            if any(skip in root for skip in [".git", "node_modules", ".venv", "__pycache__"]):
                continue

            for file in files:
                if not file.endswith((".py", ".js", ".ts", ".java", ".go", ".rs")):
                    continue

                file_path = Path(root) / file
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            match = todo_pattern.search(line)
                            if match:
                                todo_type, description = match.groups()
                                issues.append(
                                    Issue(
                                        title=f"{todo_type} in {file}",
                                        description=description.strip(),
                                        severity=Severity.LOW,
                                        source=f"{file}:{line_num}",
                                    )
                                )
                except Exception:
                    continue

        return issues

    def _check_for_security_issues(self, repo_path: str) -> List[Issue]:
        """Basic security issue detection.

        Args:
            repo_path: Path to repository root

        Returns:
            List of potential security issues
        """
        issues: List[Issue] = []

        # Patterns that might indicate security issues
        security_patterns = [
            (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password detected"),
            (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API key detected"),
            (r"secret\s*=\s*['\"][^'\"]+['\"]", "Hardcoded secret detected"),
            (r"eval\s*\(", "Use of eval() detected"),
            (r"exec\s*\(", "Use of exec() detected"),
        ]

        for root, _, files in os.walk(repo_path):
            if any(skip in root for skip in [".git", "node_modules", ".venv", "__pycache__", "tests", "test"]):
                continue

            for file in files:
                if not file.endswith((".py", ".js", ".ts", ".java")):
                    continue

                file_path = Path(root) / file
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for pattern, description in security_patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                issues.append(
                                    Issue(
                                        title=f"Potential security issue in {file}",
                                        description=description,
                                        severity=Severity.HIGH,
                                        source=str(file_path.relative_to(repo_path)),
                                    )
                                )
                except Exception:
                    continue

        return issues

