"""Compliance reporting for SOC2, HIPAA, PCI-DSS."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


class ComplianceFramework(Enum):
    """Compliance frameworks."""

    SOC2 = "soc2"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    ISO27001 = "iso27001"


@dataclass
class ComplianceControl:
    """A compliance control requirement."""

    control_id: str
    name: str
    description: str
    framework: ComplianceFramework
    severity: str
    category: str
    requirements: List[str] = field(default_factory=list)


@dataclass
class ComplianceViolation:
    """A compliance violation."""

    control: ComplianceControl
    file_path: str
    line_number: int
    description: str
    remediation: str
    evidence: str


@dataclass
class ComplianceReport:
    """Compliance report for a framework."""

    framework: ComplianceFramework
    total_controls: int
    passing_controls: int
    failing_controls: int
    violations: List[ComplianceViolation] = field(default_factory=list)
    compliance_score: float = 0.0

    def __post_init__(self):
        """Calculate compliance score."""
        if self.total_controls > 0:
            self.compliance_score = (self.passing_controls / self.total_controls) * 100


class ComplianceReporter:
    """Generate compliance reports."""

    # SOC2 Trust Service Criteria
    SOC2_CONTROLS = [
        ComplianceControl(
            control_id="CC6.1",
            name="Logical and Physical Access Controls",
            description="The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events to meet the entity's objectives.",
            framework=ComplianceFramework.SOC2,
            severity="high",
            category="access_control",
            requirements=[
                "No hardcoded credentials",
                "Secure authentication mechanisms",
                "Access logging and monitoring",
            ],
        ),
        ComplianceControl(
            control_id="CC6.6",
            name="Encryption of Data",
            description="The entity implements encryption to protect data at rest and in transit.",
            framework=ComplianceFramework.SOC2,
            severity="high",
            category="encryption",
            requirements=[
                "Use strong encryption algorithms",
                "No weak crypto (MD5, SHA1)",
                "Secure key management",
            ],
        ),
        ComplianceControl(
            control_id="CC7.2",
            name="Detection of Security Events",
            description="The entity monitors system components and the operation of those components for anomalies that are indicative of malicious acts, natural disasters, and errors affecting the entity's ability to meet its objectives.",
            framework=ComplianceFramework.SOC2,
            severity="medium",
            category="monitoring",
            requirements=[
                "Logging of security events",
                "Error handling and reporting",
                "Audit trail implementation",
            ],
        ),
    ]

    # HIPAA Security Rule
    HIPAA_CONTROLS = [
        ComplianceControl(
            control_id="164.312(a)(1)",
            name="Access Control",
            description="Implement technical policies and procedures for electronic information systems that maintain electronic protected health information to allow access only to those persons or software programs that have been granted access rights.",
            framework=ComplianceFramework.HIPAA,
            severity="critical",
            category="access_control",
            requirements=[
                "Unique user identification",
                "Emergency access procedure",
                "Automatic logoff",
                "Encryption and decryption",
            ],
        ),
        ComplianceControl(
            control_id="164.312(e)(1)",
            name="Transmission Security",
            description="Implement technical security measures to guard against unauthorized access to electronic protected health information that is being transmitted over an electronic communications network.",
            framework=ComplianceFramework.HIPAA,
            severity="critical",
            category="encryption",
            requirements=[
                "Integrity controls",
                "Encryption of data in transit",
                "Secure communication protocols",
            ],
        ),
    ]

    # PCI-DSS Requirements
    PCI_DSS_CONTROLS = [
        ComplianceControl(
            control_id="PCI-3.4",
            name="Render PAN Unreadable",
            description="Render PAN unreadable anywhere it is stored (including on portable digital media, backup media, and in logs).",
            framework=ComplianceFramework.PCI_DSS,
            severity="critical",
            category="data_protection",
            requirements=[
                "No storage of sensitive authentication data after authorization",
                "Mask PAN when displayed",
                "Encrypt stored cardholder data",
            ],
        ),
        ComplianceControl(
            control_id="PCI-6.5.1",
            name="Injection Flaws",
            description="Injection flaws, particularly SQL injection. Also consider OS Command Injection, LDAP and XPath injection flaws as well as other injection flaws.",
            framework=ComplianceFramework.PCI_DSS,
            severity="critical",
            category="secure_coding",
            requirements=[
                "Input validation",
                "Parameterized queries",
                "Output encoding",
            ],
        ),
    ]

    def __init__(self):
        """Initialize compliance reporter."""
        self.controls = {
            ComplianceFramework.SOC2: self.SOC2_CONTROLS,
            ComplianceFramework.HIPAA: self.HIPAA_CONTROLS,
            ComplianceFramework.PCI_DSS: self.PCI_DSS_CONTROLS,
        }

    def generate_report(
        self, framework: ComplianceFramework, analysis_results: Dict
    ) -> ComplianceReport:
        """Generate compliance report.

        Args:
            framework: Compliance framework
            analysis_results: Analysis results with security findings

        Returns:
            Compliance report
        """
        controls = self.controls.get(framework, [])
        violations = []

        # Map security findings to compliance violations
        security_issues = analysis_results.get("security_issues", [])

        for control in controls:
            # Check if any security issues violate this control
            control_violations = self._check_control(control, security_issues)
            violations.extend(control_violations)

        passing = len(controls) - len(set(v.control.control_id for v in violations))
        failing = len(set(v.control.control_id for v in violations))

        return ComplianceReport(
            framework=framework,
            total_controls=len(controls),
            passing_controls=passing,
            failing_controls=failing,
            violations=violations,
        )

    def _check_control(
        self, control: ComplianceControl, security_issues: List
    ) -> List[ComplianceViolation]:
        """Check if control is violated.

        Args:
            control: Compliance control
            security_issues: List of security issues

        Returns:
            List of violations
        """
        violations = []

        # Map control categories to security issue patterns
        category_patterns = {
            "access_control": ["hardcoded", "password", "secret", "api_key", "token"],
            "encryption": ["md5", "sha1", "weak_crypto", "insecure_hash"],
            "data_protection": ["sensitive_data", "pii", "credit_card", "ssn"],
            "secure_coding": [
                "sql_injection",
                "xss",
                "command_injection",
                "path_traversal",
            ],
        }

        patterns = category_patterns.get(control.category, [])

        for issue in security_issues:
            issue_title = issue.title.lower() if hasattr(issue, "title") else ""
            issue_desc = (
                issue.description.lower() if hasattr(issue, "description") else ""
            )

            if any(
                pattern in issue_title or pattern in issue_desc for pattern in patterns
            ):
                violations.append(
                    ComplianceViolation(
                        control=control,
                        file_path=issue.source.split(":")[0]
                        if hasattr(issue, "source") and ":" in issue.source
                        else "unknown",
                        line_number=int(issue.source.split(":")[1])
                        if hasattr(issue, "source")
                        and ":" in issue.source
                        and len(issue.source.split(":")) > 1
                        else 0,
                        description=issue.description
                        if hasattr(issue, "description")
                        else "",
                        remediation=f"Address {control.name} requirement",
                        evidence=issue.title if hasattr(issue, "title") else "",
                    )
                )

        return violations
