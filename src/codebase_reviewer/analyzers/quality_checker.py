"""Code quality checking and issue detection."""

import os
import re
from pathlib import Path
from typing import List

from codebase_reviewer.models import Issue, Severity
from codebase_reviewer.security.rule_engine import RuleEngine, Finding
from codebase_reviewer.security.rules_loader import RulesLoader


class QualityChecker:
    """Performs code quality checks and detects common issues."""

    def __init__(self):
        """Initialize quality checker with security scanner."""
        self.security_engine = RuleEngine(RulesLoader.get_builtin_rules())

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

        # Check for basic security issues (legacy patterns)
        issues.extend(self._check_for_security_issues(repo_path))

        # Run comprehensive security scan with OWASP rules
        issues.extend(self._run_security_scan(repo_path))

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

    def _run_security_scan(self, repo_path: str) -> List[Issue]:
        """Run comprehensive security scan using OWASP rules.

        Args:
            repo_path: Path to repository root

        Returns:
            List of security issues found
        """
        issues: List[Issue] = []

        # Build language map for files
        language_map = self._build_language_map(repo_path)

        # Scan the entire directory
        findings = self.security_engine.scan_directory(Path(repo_path), language_map)

        # Convert Finding to Issue
        for finding in findings:
            issues.append(
                Issue(
                    title=f"{finding.rule_name}",
                    description=f"{finding.description}\n\nRemediation: {finding.remediation}\n\nCode: {finding.line_content}",
                    severity=self._convert_severity(finding.severity),
                    source=f"{finding.file_path}:{finding.line_number}",
                )
            )

        return issues

    def _build_language_map(self, repo_path: str) -> dict:
        """Build a mapping of file paths to programming languages.

        Args:
            repo_path: Path to repository root

        Returns:
            Dictionary mapping file paths to language names
        """
        language_map = {}

        # Extension to language mapping
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.java': 'java',
            '.cs': 'csharp',
            '.rb': 'ruby',
            '.go': 'go',
            '.php': 'php',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp',
        }

        # Walk the directory
        for root, _, files in os.walk(repo_path):
            # Skip common directories
            if any(skip in root for skip in ['.git', 'node_modules', '.venv', '__pycache__', 'venv', 'env']):
                continue

            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                if ext in ext_to_lang:
                    language_map[str(file_path)] = ext_to_lang[ext]

        return language_map

    def _convert_severity(self, security_severity) -> Severity:
        """Convert security severity to Issue severity.

        Args:
            security_severity: Security rule severity enum

        Returns:
            Severity enum value
        """
        # Get the string value from the security Severity enum
        severity_value = security_severity.value if hasattr(security_severity, 'value') else str(security_severity)

        severity_map = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
        }
        return severity_map.get(severity_value.lower(), Severity.MEDIUM)
