"""
Quality rule engine for pattern-based code quality detection.

This module provides a flexible rule engine that can detect code quality issues
using regex patterns and metrics.
"""

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Pattern
import logging

logger = logging.getLogger(__name__)


class QualitySeverity(Enum):
    """Severity levels for quality findings."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

    def __lt__(self, other):
        """Allow severity comparison for sorting."""
        order = {
            QualitySeverity.HIGH: 0,
            QualitySeverity.MEDIUM: 1,
            QualitySeverity.LOW: 2,
            QualitySeverity.INFO: 3,
        }
        return order[self] < order[other]


@dataclass
class QualityRule:
    """A quality rule for detecting code quality issues."""

    id: str
    name: str
    description: str
    severity: QualitySeverity
    pattern: str
    languages: List[str]
    category: str  # complexity, maintainability, style, documentation
    remediation: str = ""
    code_example: str = ""
    effort_minutes: int = 15
    compiled_pattern: Optional[Pattern] = None

    def __post_init__(self):
        """Compile the regex pattern after initialization."""
        try:
            self.compiled_pattern = re.compile(self.pattern, re.MULTILINE)
        except re.error as e:
            logger.error(f"Failed to compile pattern for rule {self.id}: {e}")
            self.compiled_pattern = None


@dataclass
class QualityFinding:
    """A quality finding from applying a rule."""

    rule_id: str
    rule_name: str
    severity: QualitySeverity
    file_path: str
    line_number: int
    line_content: str
    description: str
    remediation: str
    code_example: str
    category: str
    effort_minutes: int = 15


class QualityEngine:
    """Engine for scanning code with quality rules."""

    def __init__(self, rules: List[QualityRule]):
        """Initialize the quality engine with rules."""
        self.rules = rules
        self.findings: List[QualityFinding] = []
        logger.info(f"Initialized QualityEngine with {len(rules)} rules")

    def scan_file(self, file_path: Path, language: str) -> List[QualityFinding]:
        """Scan a single file for quality issues."""
        findings = []

        # Filter rules by language
        applicable_rules = [
            r for r in self.rules if language in r.languages and r.compiled_pattern
        ]

        if not applicable_rules:
            return findings

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for rule in applicable_rules:
                for line_num, line in enumerate(lines, 1):
                    if rule.compiled_pattern.search(line):
                        findings.append(
                            QualityFinding(
                                rule_id=rule.id,
                                rule_name=rule.name,
                                severity=rule.severity,
                                file_path=str(file_path),
                                line_number=line_num,
                                line_content=line.strip(),
                                description=rule.description,
                                remediation=rule.remediation,
                                code_example=rule.code_example,
                                category=rule.category,
                                effort_minutes=rule.effort_minutes,
                            )
                        )

        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")

        # Store findings for later retrieval
        self.findings.extend(findings)
        return findings

    def scan_directory(
        self, directory: Path, language_map: Dict[str, str]
    ) -> List[QualityFinding]:
        """Scan a directory for quality issues."""
        all_findings = []

        for file_path_str, language in language_map.items():
            file_path = Path(file_path_str)
            if file_path.exists() and file_path.is_file():
                findings = self.scan_file(file_path, language)
                all_findings.extend(findings)

        self.findings = all_findings
        logger.info(f"Scan complete: {len(all_findings)} findings")
        return all_findings

    def get_findings_by_severity(self) -> Dict[QualitySeverity, List[QualityFinding]]:
        """Group findings by severity level."""
        grouped = {severity: [] for severity in QualitySeverity}
        for finding in self.findings:
            grouped[finding.severity].append(finding)
        return grouped

    def get_findings_by_category(self) -> Dict[str, List[QualityFinding]]:
        """Group findings by category."""
        grouped = {}
        for finding in self.findings:
            if finding.category not in grouped:
                grouped[finding.category] = []
            grouped[finding.category].append(finding)
        return grouped
