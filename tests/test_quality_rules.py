"""Tests for quality rule engine and loader."""

import pytest
from pathlib import Path
import tempfile

from codebase_reviewer.quality.quality_engine import (
    QualityEngine,
    QualityRule,
    QualitySeverity,
    QualityFinding,
)
from codebase_reviewer.quality.quality_loader import QualityRulesLoader


class TestQualityEngine:
    """Test the quality rule engine."""

    def test_rule_creation(self):
        """Test creating a quality rule."""
        rule = QualityRule(
            id="test-rule",
            name="Test Rule",
            description="A test rule",
            severity=QualitySeverity.MEDIUM,
            pattern=r"TODO:",
            languages=["python"],
            category="documentation",
        )
        assert rule.id == "test-rule"
        assert rule.severity == QualitySeverity.MEDIUM
        assert rule.compiled_pattern is not None

    def test_scan_file_with_finding(self):
        """Test scanning a file that has a quality issue."""
        rule = QualityRule(
            id="todo-check",
            name="TODO Comment",
            description="Found TODO comment",
            severity=QualitySeverity.LOW,
            pattern=r"# TODO:",
            languages=["python"],
            category="documentation",
        )
        engine = QualityEngine([rule])

        # Create temp file with TODO
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("# TODO: Fix this\n")
            f.write("def foo():\n")
            f.write("    pass\n")
            temp_path = Path(f.name)

        try:
            findings = engine.scan_file(temp_path, "python")
            assert len(findings) == 1
            assert findings[0].rule_id == "todo-check"
            assert findings[0].line_number == 1
        finally:
            temp_path.unlink()

    def test_scan_file_no_finding(self):
        """Test scanning a file with no issues."""
        rule = QualityRule(
            id="todo-check",
            name="TODO Comment",
            description="Found TODO comment",
            severity=QualitySeverity.LOW,
            pattern=r"# TODO:",
            languages=["python"],
            category="documentation",
        )
        engine = QualityEngine([rule])

        # Create temp file without TODO
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("def foo():\n")
            f.write("    pass\n")
            temp_path = Path(f.name)

        try:
            findings = engine.scan_file(temp_path, "python")
            assert len(findings) == 0
        finally:
            temp_path.unlink()

    def test_language_filtering(self):
        """Test that rules are filtered by language."""
        rule = QualityRule(
            id="python-only",
            name="Python Only Rule",
            description="Only applies to Python",
            severity=QualitySeverity.LOW,
            pattern=r"# TODO:",
            languages=["python"],
            category="documentation",
        )
        engine = QualityEngine([rule])

        # Create temp JavaScript file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            f.write("// TODO: Fix this\n")
            temp_path = Path(f.name)

        try:
            findings = engine.scan_file(temp_path, "javascript")
            assert len(findings) == 0  # Rule doesn't apply to JavaScript
        finally:
            temp_path.unlink()

    def test_severity_comparison(self):
        """Test severity level comparison."""
        assert QualitySeverity.HIGH < QualitySeverity.MEDIUM
        assert QualitySeverity.MEDIUM < QualitySeverity.LOW
        assert QualitySeverity.LOW < QualitySeverity.INFO

    def test_get_findings_by_severity(self):
        """Test grouping findings by severity."""
        rules = [
            QualityRule(
                id="high-rule",
                name="High Severity",
                description="High severity issue",
                severity=QualitySeverity.HIGH,
                pattern=r"FIXME:",
                languages=["python"],
                category="maintainability",
            ),
            QualityRule(
                id="low-rule",
                name="Low Severity",
                description="Low severity issue",
                severity=QualitySeverity.LOW,
                pattern=r"TODO:",
                languages=["python"],
                category="documentation",
            ),
        ]
        engine = QualityEngine(rules)

        # Create temp file with both issues
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("# TODO: Fix this\n")
            f.write("# FIXME: Broken\n")
            temp_path = Path(f.name)

        try:
            engine.scan_file(temp_path, "python")
            by_severity = engine.get_findings_by_severity()
            assert len(by_severity[QualitySeverity.HIGH]) == 1
            assert len(by_severity[QualitySeverity.LOW]) == 1
        finally:
            temp_path.unlink()


class TestQualityRulesLoader:
    """Test the quality rules loader."""

    def test_load_builtin_rules(self):
        """Test loading built-in quality rules."""
        rules = QualityRulesLoader.get_builtin_rules()
        assert len(rules) > 0
        assert all(isinstance(r, QualityRule) for r in rules)

    def test_rule_has_required_fields(self):
        """Test that all built-in rules have required fields."""
        rules = QualityRulesLoader.get_builtin_rules()
        for rule in rules:
            assert rule.id
            assert rule.name
            assert rule.description
            assert rule.severity
            assert rule.pattern
            assert rule.languages
            assert rule.category
