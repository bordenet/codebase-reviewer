"""Data models for v2.0 prompt schemas."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(Enum):
    """Overall security risk level."""

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class QualityGateStatus(Enum):
    """Quality gate pass/fail status."""

    PASS = "Pass"
    FAIL = "Fail"


class FindingCategory(Enum):
    """Category of finding."""

    SECURITY = "security"
    QUALITY = "quality"
    ARCHITECTURE = "architecture"


class Severity(Enum):
    """Severity level for findings."""

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"


class Confidence(Enum):
    """Confidence level for findings."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class CheckStatus(Enum):
    """Status of a security check."""

    PASS = "Pass"
    FAIL = "Fail"
    WARNING = "Warning"


@dataclass
class Finding:
    """A security, quality, or architecture finding."""

    id: str
    category: FindingCategory
    severity: Severity
    confidence: Confidence
    description: str
    remediation_summary: str
    owasp_category: Optional[str] = None
    cwe_id: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class AnalysisSummary:
    """Summary of comprehensive analysis (T1 output)."""

    overall_security_risk: RiskLevel
    quality_gate_status: QualityGateStatus
    key_findings: List[Finding] = field(default_factory=list)


@dataclass
class ComprehensiveAnalysis:
    """Complete T1 output schema."""

    summary: AnalysisSummary
    architecture: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    test_coverage: str = "Not Enough Information"  # or number
    nested_repos_details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MaterialPlan:
    """A single material to be generated (T2 output)."""

    name: str
    description: str
    importance: str  # Critical/High/Medium/Low
    target_audience: str
    effort_estimate: str


@dataclass
class MaterialsPlan:
    """Complete T2 output schema."""

    materials: List[MaterialPlan] = field(default_factory=list)


@dataclass
class CLIFlag:
    """CLI flag specification."""

    flag: str
    description: str


@dataclass
class ObsolescenceChecks:
    """Self-obsolescence detection configuration."""

    file_existence: List[str] = field(default_factory=list)
    git_diff_threshold: int = 30
    structural_changes: str = ""


@dataclass
class ToolSpecification:
    """Specification for a Phase 2 tool (T3 output)."""

    name: str
    description: str
    cli_flags: List[CLIFlag] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    internal_modules: List[str] = field(default_factory=list)
    self_obsolescence_checks: Optional[ObsolescenceChecks] = None


@dataclass
class ToolsSpecification:
    """Complete T3 output schema."""

    tools: List[ToolSpecification] = field(default_factory=list)


@dataclass
class ValidationCheck:
    """A validation check specification."""

    type: str  # schema_validation, consistency_check, etc.
    details: Optional[str] = None
    schema_ref: Optional[str] = None


@dataclass
class OutputSpec:
    """Output file specification."""

    path: str
    format: str  # md, json, svg, mermaid


@dataclass
class ToolCommand:
    """Tool command specification for validation (T5 output)."""

    tool_name: str
    command: str
    required_flags: List[str] = field(default_factory=list)
    outputs: List[OutputSpec] = field(default_factory=list)
    validation_checks: List[ValidationCheck] = field(default_factory=list)


@dataclass
class ValidationPlan:
    """Complete T5 output schema."""

    tool_commands: List[ToolCommand] = field(default_factory=list)


@dataclass
class SecurityCheck:
    """A security validation check (T6 output)."""

    check_name: str
    status: CheckStatus
    details: Optional[str] = None


@dataclass
class SecurityValidationReport:
    """Complete T6 output schema."""

    security_checks: List[SecurityCheck] = field(default_factory=list)


# ========== Metrics Tracking Models (Phase 2) ==========


@dataclass
class CoverageMetrics:
    """Coverage metrics for obsolescence detection."""

    files_total: int = 0
    files_analyzed: int = 0
    files_documented: int = 0
    coverage_percent: float = 0.0


@dataclass
class ChangeMetrics:
    """Change detection metrics."""

    files_changed: int = 0
    files_changed_percent: float = 0.0
    files_added: int = 0
    files_deleted: int = 0
    new_languages: List[str] = field(default_factory=list)


@dataclass
class QualityMetrics:
    """Quality metrics."""

    error_count: int = 0
    error_rate_percent: float = 0.0
    warning_count: int = 0
    false_positive_estimate: int = 0


@dataclass
class PerformanceMetrics:
    """Performance metrics."""

    avg_runtime_seconds: float = 0.0
    memory_usage_mb: float = 0.0


@dataclass
class StalenessMetrics:
    """Staleness tracking."""

    last_run_date: str = ""  # RFC3339 format
    days_since_last_run: int = 0


@dataclass
class PatternMetrics:
    """Pattern detection metrics."""

    detected: List[str] = field(default_factory=list)
    newly_detected: List[str] = field(default_factory=list)


@dataclass
class TestMetrics:
    """Test execution metrics."""

    regression_pass_count: int = 0
    regression_fail_count: int = 0


@dataclass
class UserFeedbackMetrics:
    """User feedback tracking."""

    human_override_flags: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class Metrics:
    """Complete metrics structure for obsolescence detection."""

    coverage: CoverageMetrics = field(default_factory=CoverageMetrics)
    changes: ChangeMetrics = field(default_factory=ChangeMetrics)
    quality: QualityMetrics = field(default_factory=QualityMetrics)
    performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    staleness: StalenessMetrics = field(default_factory=StalenessMetrics)
    patterns: PatternMetrics = field(default_factory=PatternMetrics)
    tests: TestMetrics = field(default_factory=TestMetrics)
    user_feedback: UserFeedbackMetrics = field(default_factory=UserFeedbackMetrics)


# ========== Learning Capture Models ==========


@dataclass
class LearningEntry:
    """A single learning entry from tool execution."""

    id: str
    description: str
    impact: str  # positive, neutral, negative
    actions_taken: List[str] = field(default_factory=list)
    validation: str = ""
    pending_issues: str = ""


@dataclass
class LearningCapture:
    """Collection of learnings from tool execution."""

    entries: List[LearningEntry] = field(default_factory=list)
