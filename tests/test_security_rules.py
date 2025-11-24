"""Tests for security rule engine."""

import pytest
from pathlib import Path
import tempfile

from codebase_reviewer.security.rule_engine import (
    RuleEngine,
    SecurityRule,
    Severity,
    Finding,
)
from codebase_reviewer.security.rules_loader import RulesLoader


class TestRuleEngine:
    """Test the security rule engine."""

    def test_rule_creation(self):
        """Test creating a security rule."""
        rule = SecurityRule(
            id="test-rule",
            name="Test Rule",
            description="A test rule",
            severity=Severity.HIGH,
            pattern=r"password\s*=\s*['\"]",
            languages=["python"],
            owasp_category="A07:2021",
        )
        
        assert rule.id == "test-rule"
        assert rule.severity == Severity.HIGH
        assert rule.compiled_pattern is not None

    def test_scan_file_with_finding(self):
        """Test scanning a file that contains a vulnerability."""
        rule = SecurityRule(
            id="hardcoded-password",
            name="Hardcoded Password",
            description="Password hardcoded in source",
            severity=Severity.CRITICAL,
            pattern=r'password\s*=\s*["\'][^"\']+["\']',
            languages=["python"],
            owasp_category="A07:2021",
        )
        
        engine = RuleEngine([rule])
        
        # Create a temporary file with vulnerable code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('password = "MySecretPassword123"\n')
            f.write('username = "admin"\n')
            temp_path = Path(f.name)
        
        try:
            findings = engine.scan_file(temp_path, "python")
            
            assert len(findings) == 1
            assert findings[0].rule_id == "hardcoded-password"
            assert findings[0].severity == Severity.CRITICAL
            assert findings[0].line_number == 1
        finally:
            temp_path.unlink()

    def test_scan_file_no_finding(self):
        """Test scanning a file with no vulnerabilities."""
        rule = SecurityRule(
            id="hardcoded-password",
            name="Hardcoded Password",
            description="Password hardcoded in source",
            severity=Severity.CRITICAL,
            pattern=r'password\s*=\s*["\'][^"\']+["\']',
            languages=["python"],
            owasp_category="A07:2021",
        )
        
        engine = RuleEngine([rule])
        
        # Create a temporary file with safe code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('import os\n')
            f.write('password = os.environ.get("PASSWORD")\n')
            temp_path = Path(f.name)
        
        try:
            findings = engine.scan_file(temp_path, "python")
            
            assert len(findings) == 0
        finally:
            temp_path.unlink()

    def test_language_filtering(self):
        """Test that rules are only applied to matching languages."""
        rule = SecurityRule(
            id="python-only",
            name="Python Only Rule",
            description="Only applies to Python",
            severity=Severity.HIGH,
            pattern=r"test",
            languages=["python"],
            owasp_category="Test",
        )
        
        engine = RuleEngine([rule])
        
        # Create a JavaScript file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write('const test = "test";\n')
            temp_path = Path(f.name)
        
        try:
            findings = engine.scan_file(temp_path, "javascript")
            
            # Should not find anything because rule is Python-only
            assert len(findings) == 0
        finally:
            temp_path.unlink()

    def test_severity_comparison(self):
        """Test severity level comparison."""
        assert Severity.CRITICAL < Severity.HIGH
        assert Severity.HIGH < Severity.MEDIUM
        assert Severity.MEDIUM < Severity.LOW
        assert Severity.LOW < Severity.INFO

    def test_get_findings_by_severity(self):
        """Test grouping findings by severity."""
        rules = [
            SecurityRule(
                id="critical-rule",
                name="Critical",
                description="Critical",
                severity=Severity.CRITICAL,
                pattern=r"critical",
                languages=["python"],
                owasp_category="Test",
            ),
            SecurityRule(
                id="high-rule",
                name="High",
                description="High",
                severity=Severity.HIGH,
                pattern=r"high",
                languages=["python"],
                owasp_category="Test",
            ),
        ]
        
        engine = RuleEngine(rules)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('critical = True\n')
            f.write('high = True\n')
            temp_path = Path(f.name)
        
        try:
            engine.scan_file(temp_path, "python")
            grouped = engine.get_findings_by_severity()
            
            assert len(grouped[Severity.CRITICAL]) == 1
            assert len(grouped[Severity.HIGH]) == 1
            assert len(grouped[Severity.MEDIUM]) == 0
        finally:
            temp_path.unlink()


class TestRulesLoader:
    """Test the rules loader."""

    def test_load_builtin_rules(self):
        """Test loading built-in rules."""
        rules = RulesLoader.get_builtin_rules()
        
        # Should have loaded our 50+ rules
        assert len(rules) >= 50
        
        # Check that we have rules from different categories
        rule_ids = [rule.id for rule in rules]
        assert any('sql-injection' in rid for rid in rule_ids)
        assert any('xss' in rid for rid in rule_ids)
        assert any('hardcoded' in rid for rid in rule_ids)

    def test_rule_has_required_fields(self):
        """Test that loaded rules have all required fields."""
        rules = RulesLoader.get_builtin_rules()
        
        for rule in rules:
            assert rule.id
            assert rule.name
            assert rule.description
            assert rule.severity
            assert rule.pattern
            assert rule.languages
            assert rule.owasp_category
            assert rule.compiled_pattern is not None

