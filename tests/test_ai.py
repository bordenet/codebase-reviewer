"""Tests for AI module."""

import pytest

from codebase_reviewer.ai.fix_generator import CodeFix, FixGenerator
from codebase_reviewer.ai.query_interface import QueryInterface


class TestFixGenerator:
    """Tests for FixGenerator."""

    def test_initialization(self):
        """Test fix generator initialization."""
        generator = FixGenerator()
        assert generator.fix_patterns is not None
        assert len(generator.fix_patterns) > 0

    def test_generate_fix_sql_injection(self):
        """Test generating fix for SQL injection."""
        generator = FixGenerator()

        code_line = 'query = "SELECT * FROM users WHERE id = " + user_id'
        fix = generator.generate_fix("SEC-001", "test.py", 10, code_line)

        assert fix is not None
        assert fix.issue_id == "SEC-001"
        assert fix.file_path == "test.py"
        assert fix.line_number == 10
        assert fix.confidence >= 0.9
        assert fix.fix_type == "auto"
        assert "parameterized" in fix.explanation.lower()

    def test_generate_fix_hardcoded_password(self):
        """Test generating fix for hardcoded password."""
        generator = FixGenerator()

        code_line = 'password = "secret123"'
        fix = generator.generate_fix("SEC-003", "config.py", 5, code_line)

        assert fix is not None
        assert fix.issue_id == "SEC-003"
        assert "environ" in fix.fixed_code
        assert fix.confidence >= 0.9
        assert fix.fix_type == "auto"

    def test_generate_fix_api_key(self):
        """Test generating fix for hardcoded API key."""
        generator = FixGenerator()

        code_line = 'api_key = "sk-1234567890abcdef"'
        fix = generator.generate_fix("SEC-004", "api.py", 3, code_line)

        assert fix is not None
        assert "environ" in fix.fixed_code
        assert fix.confidence >= 0.9

    def test_generate_fix_todo_comment(self):
        """Test generating fix for TODO comment."""
        generator = FixGenerator()

        code_line = "# TODO: Implement error handling"
        fix = generator.generate_fix("QUAL-001", "main.py", 20, code_line)

        assert fix is not None
        assert "FIXME" in fix.fixed_code or fix.confidence < 0.9

    def test_generate_fix_no_pattern(self):
        """Test generating fix when no pattern matches."""
        generator = FixGenerator()

        code_line = "x = 1 + 2"
        fix = generator.generate_fix("UNKNOWN-001", "test.py", 1, code_line)

        assert fix is None

    def test_generate_fixes_multiple(self):
        """Test generating fixes for multiple issues."""
        generator = FixGenerator()

        issues = [
            {
                "rule_id": "SEC-003",
                "file_path": "config.py",
                "line_number": 5,
                "code_snippet": 'password = "secret123"',
            },
            {
                "rule_id": "SEC-004",
                "file_path": "api.py",
                "line_number": 3,
                "code_snippet": 'api_key = "sk-1234567890abcdef"',
            },
        ]

        fixes = generator.generate_fixes(issues)

        assert len(fixes) == 2
        assert all(isinstance(fix, CodeFix) for fix in fixes)

    def test_code_fix_to_dict(self):
        """Test CodeFix to_dict conversion."""
        fix = CodeFix(
            issue_id="SEC-003",
            file_path="test.py",
            line_number=10,
            original_code='password = "secret"',
            fixed_code='password = os.environ.get("PASSWORD")',
            fix_type="auto",
            confidence=0.95,
            explanation="Move to environment variable",
            diff="--- original\n+++ fixed\n...",
        )

        data = fix.to_dict()

        assert data["issue_id"] == "SEC-003"
        assert data["confidence"] == 0.95
        assert data["fix_type"] == "auto"


class TestQueryInterface:
    """Tests for QueryInterface."""

    def test_initialization(self):
        """Test query interface initialization."""
        interface = QueryInterface()
        assert interface.query_patterns is not None
        assert len(interface.query_patterns) > 0

    def test_query_sql_injection(self):
        """Test querying for SQL injection issues."""
        interface = QueryInterface()

        issues = [
            {
                "rule_id": "SEC-001",
                "description": "SQL injection vulnerability",
                "severity": "critical",
            },
            {
                "rule_id": "SEC-002",
                "description": "XSS vulnerability",
                "severity": "high",
            },
            {"rule_id": "QUAL-001", "description": "TODO comment", "severity": "low"},
        ]

        result = interface.query("Show me all SQL injection vulnerabilities", issues)

        assert result["success"] is True
        assert result["count"] == 1
        assert len(result["issues"]) == 1
        assert result["issues"][0]["rule_id"] == "SEC-001"

    def test_query_critical_issues(self):
        """Test querying for critical issues."""
        interface = QueryInterface()

        issues = [
            {"rule_id": "SEC-001", "severity": "critical"},
            {"rule_id": "SEC-002", "severity": "high"},
            {"rule_id": "SEC-003", "severity": "critical"},
        ]

        result = interface.query("Show me all critical issues", issues)

        assert result["success"] is True
        assert result["count"] == 2

    def test_query_security_issues(self):
        """Test querying for security issues."""
        interface = QueryInterface()

        issues = [
            {"rule_id": "SEC-001", "severity": "critical"},
            {"rule_id": "QUAL-001", "severity": "low"},
            {"rule_id": "SEC-002", "severity": "high"},
        ]

        result = interface.query("Find all security vulnerabilities", issues)

        assert result["success"] is True
        assert result["count"] == 2

    def test_query_count_only(self):
        """Test count-only query."""
        interface = QueryInterface()

        issues = [
            {"rule_id": "SEC-001"},
            {"rule_id": "SEC-002"},
            {"rule_id": "QUAL-001"},
        ]

        result = interface.query("How many total issues?", issues)

        assert result["success"] is True
        assert result["count"] == 3
        assert len(result["issues"]) == 0  # Count-only, no issues returned

    def test_query_worst_file(self):
        """Test worst file query."""
        interface = QueryInterface()

        issues = [
            {"rule_id": "SEC-001", "file_path": "main.py"},
            {"rule_id": "SEC-002", "file_path": "main.py"},
            {"rule_id": "QUAL-001", "file_path": "utils.py"},
        ]

        result = interface.query("What's the worst file?", issues)

        assert result["success"] is True
        assert result["file_path"] == "main.py"
        assert result["count"] == 2

    def test_query_unknown(self):
        """Test unknown query."""
        interface = QueryInterface()

        issues = []

        result = interface.query("This is not a valid query", issues)

        assert result["success"] is False
        assert "Could not understand" in result["message"]

    def test_get_suggestions(self):
        """Test getting query suggestions."""
        interface = QueryInterface()

        suggestions = interface.get_suggestions()

        assert len(suggestions) > 0
        assert all(isinstance(s, str) for s in suggestions)
