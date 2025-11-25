"""Tests for compliance reporting."""

import pytest
from codebase_reviewer.compliance.compliance_reporter import (
    ComplianceFramework,
    ComplianceReporter,
    ComplianceControl,
)
from codebase_reviewer.models import Issue, Severity


class TestComplianceReporter:
    """Tests for ComplianceReporter."""

    def test_initialization(self):
        """Test compliance reporter initialization."""
        reporter = ComplianceReporter()
        assert reporter is not None
        assert ComplianceFramework.SOC2 in reporter.controls
        assert ComplianceFramework.HIPAA in reporter.controls
        assert ComplianceFramework.PCI_DSS in reporter.controls

    def test_soc2_controls(self):
        """Test SOC2 controls are defined."""
        reporter = ComplianceReporter()
        controls = reporter.controls[ComplianceFramework.SOC2]
        assert len(controls) > 0
        assert any(c.control_id == "CC6.1" for c in controls)

    def test_hipaa_controls(self):
        """Test HIPAA controls are defined."""
        reporter = ComplianceReporter()
        controls = reporter.controls[ComplianceFramework.HIPAA]
        assert len(controls) > 0
        assert any(c.control_id == "164.312(a)(1)" for c in controls)

    def test_pci_dss_controls(self):
        """Test PCI-DSS controls are defined."""
        reporter = ComplianceReporter()
        controls = reporter.controls[ComplianceFramework.PCI_DSS]
        assert len(controls) > 0
        assert any(c.control_id == "PCI-3.4" for c in controls)

    def test_generate_report_no_violations(self):
        """Test generating report with no violations."""
        reporter = ComplianceReporter()

        analysis_results = {"security_issues": []}

        report = reporter.generate_report(ComplianceFramework.SOC2, analysis_results)

        assert report.framework == ComplianceFramework.SOC2
        assert report.total_controls > 0
        assert report.passing_controls == report.total_controls
        assert report.failing_controls == 0
        assert len(report.violations) == 0
        assert report.compliance_score == 100.0

    def test_generate_report_with_violations(self):
        """Test generating report with violations."""
        reporter = ComplianceReporter()

        # Create security issues that violate controls
        analysis_results = {
            "security_issues": [
                Issue(
                    title="Hardcoded Password",
                    description="Hardcoded password found in code",
                    severity=Severity.CRITICAL,
                    source="config.py:10",
                ),
                Issue(
                    title="Weak Crypto",
                    description="MD5 hash used for encryption",
                    severity=Severity.HIGH,
                    source="crypto.py:20",
                ),
            ]
        }

        report = reporter.generate_report(ComplianceFramework.SOC2, analysis_results)

        assert report.framework == ComplianceFramework.SOC2
        assert report.total_controls > 0
        assert report.failing_controls > 0
        assert len(report.violations) > 0
        assert report.compliance_score < 100.0

    def test_compliance_score_calculation(self):
        """Test compliance score calculation."""
        reporter = ComplianceReporter()

        analysis_results = {
            "security_issues": [
                Issue(
                    title="SQL Injection",
                    description="SQL injection vulnerability",
                    severity=Severity.CRITICAL,
                    source="db.py:15",
                ),
            ]
        }

        report = reporter.generate_report(ComplianceFramework.PCI_DSS, analysis_results)

        # Score should be between 0 and 100
        assert 0 <= report.compliance_score <= 100

        # With violations, score should be less than 100
        if report.failing_controls > 0:
            assert report.compliance_score < 100

    def test_check_control_access_control(self):
        """Test checking access control violations."""
        reporter = ComplianceReporter()

        control = ComplianceControl(
            control_id="TEST-1",
            name="Test Control",
            description="Test",
            framework=ComplianceFramework.SOC2,
            severity="high",
            category="access_control",
        )

        security_issues = [
            Issue(
                title="Hardcoded API Key",
                description="API key hardcoded in source",
                severity=Severity.CRITICAL,
                source="api.py:5",
            ),
        ]

        violations = reporter._check_control(control, security_issues)

        assert len(violations) > 0
        assert violations[0].control.control_id == "TEST-1"

    def test_check_control_encryption(self):
        """Test checking encryption violations."""
        reporter = ComplianceReporter()

        control = ComplianceControl(
            control_id="TEST-2",
            name="Test Encryption",
            description="Test",
            framework=ComplianceFramework.HIPAA,
            severity="critical",
            category="encryption",
        )

        security_issues = [
            Issue(
                title="Weak Crypto",
                description="MD5 used for hashing",
                severity=Severity.HIGH,
                source="hash.py:10",
            ),
        ]

        violations = reporter._check_control(control, security_issues)

        assert len(violations) > 0
