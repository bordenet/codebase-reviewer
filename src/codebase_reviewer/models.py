"""Data models for Codebase Reviewer."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ClaimType(Enum):
    """Types of claims found in documentation."""

    ARCHITECTURE = "architecture"
    SETUP = "setup"
    API = "api"
    FEATURE = "feature"
    DEPENDENCY = "dependency"
    DEPLOYMENT = "deployment"


class ValidationStatus(Enum):
    """Validation result status."""

    VALID = "valid"
    INVALID = "invalid"
    PARTIAL = "partial"
    UNTESTABLE = "untestable"


class Severity(Enum):
    """Severity level for issues."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class DocumentFile:
    """Represents a documentation file in the repository."""

    path: str
    doc_type: str  # 'readme', 'contributing', 'architecture', etc.
    content: str
    priority: int  # 1=highest (README), 5=lowest
    last_modified: datetime
    size_bytes: int = 0


@dataclass
class Claim:
    """A testable claim extracted from documentation."""

    source_doc: str
    claim_type: ClaimType
    description: str
    testable: bool
    validated: Optional[ValidationStatus] = None
    validation_notes: Optional[str] = None
    severity: Severity = Severity.MEDIUM


@dataclass
class ArchitectureClaims:
    """Architecture information claimed in documentation."""

    pattern: Optional[str] = None  # "microservices", "monolith", "MVC", etc.
    layers: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)
    data_flow: Optional[str] = None
    documented_in: List[str] = field(default_factory=list)


@dataclass
class SetupGuide:
    """Installation and setup instructions from documentation."""

    prerequisites: List[str] = field(default_factory=list)
    build_steps: List[str] = field(default_factory=list)
    environment_vars: List[str] = field(default_factory=list)
    deployment_steps: List[str] = field(default_factory=list)
    documented_in: List[str] = field(default_factory=list)


@dataclass
class APISpec:
    """API documentation information."""

    endpoints: List[Dict[str, Any]] = field(default_factory=list)
    api_type: Optional[str] = None  # REST, GraphQL, gRPC, etc.
    documented_in: List[str] = field(default_factory=list)


@dataclass
class CodingStandards:
    """Coding standards and conventions from documentation."""

    style_guide: Optional[str] = None
    linting_tools: List[str] = field(default_factory=list)
    naming_conventions: List[str] = field(default_factory=list)
    documented_in: List[str] = field(default_factory=list)


@dataclass
class Issue:
    """An issue or known problem documented."""

    title: str
    description: str
    severity: Severity
    source: str


@dataclass
class DocumentationAnalysis:
    """Results of documentation analysis."""

    discovered_docs: List[DocumentFile] = field(default_factory=list)
    claimed_architecture: Optional[ArchitectureClaims] = None
    setup_instructions: Optional[SetupGuide] = None
    api_documentation: Optional[APISpec] = None
    coding_standards: Optional[CodingStandards] = None
    known_issues: List[Issue] = field(default_factory=list)
    claims: List[Claim] = field(default_factory=list)
    completeness_score: float = 0.0


@dataclass
class DirectoryTree:
    """Repository directory structure."""

    root: str
    structure: Dict[str, Any] = field(default_factory=dict)
    total_files: int = 0
    total_dirs: int = 0


@dataclass
class Language:
    """Programming language detected in repository."""

    name: str
    percentage: float
    file_count: int
    line_count: int


@dataclass
class Framework:
    """Framework detected in repository."""

    name: str
    version: Optional[str] = None
    confidence: float = 1.0


@dataclass
class EntryPoint:
    """Application entry point."""

    path: str
    entry_type: str  # main, api, cli, etc.
    description: str = ""


@dataclass
class CodeStructure:
    """Code structure analysis results."""

    languages: List[Language] = field(default_factory=list)
    frameworks: List[Framework] = field(default_factory=list)
    entry_points: List[EntryPoint] = field(default_factory=list)
    directory_tree: Optional[DirectoryTree] = None


@dataclass
class DependencyInfo:
    """Dependency information."""

    name: str
    dependency_type: str = "production"  # production, development, optional
    version: Optional[str] = None
    source_file: str = ""


@dataclass
class CodeAnalysis:
    """Complete code analysis results."""

    structure: Optional[CodeStructure] = None
    dependencies: List[DependencyInfo] = field(default_factory=list)
    complexity_metrics: Dict[str, Any] = field(default_factory=dict)
    quality_issues: List[Issue] = field(default_factory=list)
    analytics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of validating a documentation claim."""

    claim: Claim
    validation_status: ValidationStatus
    severity: Severity
    evidence: str
    recommendation: str


@dataclass
class DriftReport:
    """Documentation vs code discrepancies."""

    architecture_drift: List[ValidationResult] = field(default_factory=list)
    setup_drift: List[ValidationResult] = field(default_factory=list)
    api_drift: List[ValidationResult] = field(default_factory=list)
    undocumented_features: List[str] = field(default_factory=list)
    outdated_documentation: List[str] = field(default_factory=list)
    drift_severity: Severity = Severity.LOW


@dataclass
class Prompt:
    """Generated AI prompt."""

    prompt_id: str
    phase: int
    title: str
    context: Any
    objective: str
    tasks: List[str] = field(default_factory=list)
    deliverable: str = ""
    ai_model_hints: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    critical_findings: Optional[List[Any]] = None


@dataclass
class PromptCollection:
    """Collection of all generated prompts."""

    phase0: List[Prompt] = field(default_factory=list)
    phase1: List[Prompt] = field(default_factory=list)
    phase2: List[Prompt] = field(default_factory=list)
    phase3: List[Prompt] = field(default_factory=list)
    phase4: List[Prompt] = field(default_factory=list)

    def all_prompts(self) -> List[Prompt]:
        """Get all prompts in order."""
        return self.phase0 + self.phase1 + self.phase2 + self.phase3 + self.phase4

    def to_markdown(self) -> str:
        """Convert all prompts to markdown format."""
        lines = ["# Generated Prompts\n"]
        for i, phase_name in enumerate(["Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4"]):
            phase_prompts = getattr(self, f"phase{i}")
            if phase_prompts:
                lines.append(f"\n## {phase_name}\n")
                for prompt in phase_prompts:
                    lines.append(f"### {prompt.title}\n")
                    lines.append(f"**Objective:** {prompt.objective}\n")
                    if prompt.tasks:
                        lines.append("**Tasks:**\n")
                        for task in prompt.tasks:
                            lines.append(f"- {task}\n")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Convert all prompts to dictionary format."""

        def prompt_to_dict(p: Prompt) -> Dict[str, Any]:
            return {
                "prompt_id": p.prompt_id,
                "phase": p.phase,
                "title": p.title,
                "objective": p.objective,
                "tasks": p.tasks,
                "deliverable": p.deliverable,
            }

        return {
            "phase0": [prompt_to_dict(p) for p in self.phase0],
            "phase1": [prompt_to_dict(p) for p in self.phase1],
            "phase2": [prompt_to_dict(p) for p in self.phase2],
            "phase3": [prompt_to_dict(p) for p in self.phase3],
            "phase4": [prompt_to_dict(p) for p in self.phase4],
        }


@dataclass
class RepositoryAnalysis:
    """Complete repository analysis results."""

    repository_path: str
    documentation: Optional[DocumentationAnalysis] = None
    code: Optional[CodeAnalysis] = None
    validation: Optional[DriftReport] = None
    prompts: Optional[PromptCollection] = None
    timestamp: datetime = field(default_factory=datetime.now)
    analysis_duration_seconds: float = 0.0
