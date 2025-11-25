"""Automated fix generation for code issues."""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CodeFix:
    """Represents an automated code fix."""

    issue_id: str
    file_path: str
    line_number: int
    original_code: str
    fixed_code: str
    fix_type: str  # 'auto', 'suggested', 'manual'
    confidence: float  # 0.0 to 1.0
    explanation: str
    diff: str

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "issue_id": self.issue_id,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "original_code": self.original_code,
            "fixed_code": self.fixed_code,
            "fix_type": self.fix_type,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "diff": self.diff,
        }


class FixGenerator:
    """Generates automated fixes for code issues."""

    def __init__(self):
        """Initialize fix generator."""
        self.fix_patterns = self._load_fix_patterns()

    def _load_fix_patterns(self) -> dict:
        """Load fix patterns for common issues.

        Returns:
            Dictionary of fix patterns
        """
        return {
            # Security fixes
            "SEC-001": {  # SQL injection - string concatenation
                "pattern": r'(\w+)\s*=\s*["\']SELECT.*["\']\s*\+\s*(\w+)',
                "replacement": r'\1 = "SELECT ... WHERE id = ?" # Use parameterized query',
                "explanation": "Replace string concatenation with parameterized query",
                "confidence": 0.9,
            },
            "SEC-003": {  # Hardcoded password
                "pattern": r'password\s*=\s*["\']([^"\']+)["\']',
                "replacement": r'password = os.environ.get("PASSWORD")',
                "explanation": "Move password to environment variable",
                "confidence": 0.95,
            },
            "SEC-004": {  # Hardcoded API key
                "pattern": r'api_key\s*=\s*["\']([^"\']+)["\']',
                "replacement": r'api_key = os.environ.get("API_KEY")',
                "explanation": "Move API key to environment variable",
                "confidence": 0.95,
            },
            # Quality fixes
            "QUAL-001": {  # TODO comment
                "pattern": r"#\s*TODO:?\s*(.+)",
                "replacement": r"# FIXME: \1 (tracked in issue tracker)",
                "explanation": "Convert TODO to tracked issue",
                "confidence": 0.7,
            },
            "QUAL-003": {  # Magic number
                "pattern": r"if\s+\w+\s*[<>=!]+\s*(\d+)",
                "replacement": r"MAX_VALUE = \1  # Define constant\nif variable <= MAX_VALUE",
                "explanation": "Extract magic number to named constant",
                "confidence": 0.8,
            },
            "QUAL-010": {  # Missing docstring
                "pattern": r"def\s+(\w+)\s*\([^)]*\):",
                "replacement": r'def \1(...):\n    """TODO: Add docstring."""',
                "explanation": "Add docstring placeholder",
                "confidence": 0.6,
            },
        }

    def generate_fix(self, issue_id: str, file_path: str, line_number: int, code_line: str) -> Optional[CodeFix]:
        """Generate automated fix for an issue.

        Args:
            issue_id: Issue identifier (e.g., 'SEC-001')
            file_path: Path to file with issue
            line_number: Line number of issue
            code_line: Original code line

        Returns:
            CodeFix if fix can be generated, None otherwise
        """
        # Check if we have a fix pattern for this issue
        if issue_id not in self.fix_patterns:
            return None

        pattern_info = self.fix_patterns[issue_id]
        pattern = pattern_info["pattern"]
        replacement = pattern_info["replacement"]

        # Try to apply the fix pattern
        if not re.search(pattern, code_line):
            return None

        # Generate fixed code
        fixed_code = re.sub(pattern, replacement, code_line)

        # Generate diff
        diff = self._generate_diff(code_line, fixed_code, line_number)

        # Determine fix type based on confidence
        confidence = pattern_info["confidence"]
        if confidence >= 0.9:
            fix_type = "auto"
        elif confidence >= 0.7:
            fix_type = "suggested"
        else:
            fix_type = "manual"

        return CodeFix(
            issue_id=issue_id,
            file_path=file_path,
            line_number=line_number,
            original_code=code_line.strip(),
            fixed_code=fixed_code.strip(),
            fix_type=fix_type,
            confidence=confidence,
            explanation=pattern_info["explanation"],
            diff=diff,
        )

    def generate_fixes(self, issues: List[dict]) -> List[CodeFix]:
        """Generate fixes for multiple issues.

        Args:
            issues: List of issues to fix

        Returns:
            List of generated fixes
        """
        fixes = []

        for issue in issues:
            # Extract issue details
            issue_id = issue.get("rule_id", "")
            file_path = issue.get("file_path", "")
            line_number = issue.get("line_number", 0)

            # Read the code line (simplified - in real implementation, read from file)
            code_line = issue.get("code_snippet", "")

            if code_line:
                fix = self.generate_fix(issue_id, file_path, line_number, code_line)
                if fix:
                    fixes.append(fix)

        return fixes

    def _generate_diff(self, original: str, fixed: str, line_number: int) -> str:
        """Generate unified diff format.

        Args:
            original: Original code
            fixed: Fixed code
            line_number: Line number

        Returns:
            Diff string
        """
        return f"""--- original
+++ fixed
@@ -{line_number},1 +{line_number},1 @@
-{original.strip()}
+{fixed.strip()}"""
