"""
Security rule engine for pattern-based vulnerability detection.

This module provides a flexible rule engine that can detect security vulnerabilities
using regex patterns, similar to Semgrep but simpler.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Pattern
import logging

logger = logging.getLogger(__name__)


class Severity(Enum):
    """Severity levels for security findings."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

    def __lt__(self, other):
        """Allow severity comparison for sorting."""
        order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.INFO: 4,
        }
        return order[self] < order[other]


@dataclass
class SecurityRule:
    """A security rule for detecting vulnerabilities."""
    id: str
    name: str
    description: str
    severity: Severity
    pattern: str
    languages: List[str]
    owasp_category: str
    cwe_id: Optional[str] = None
    remediation: str = ""
    code_example: str = ""
    effort_minutes: int = 30
    compiled_pattern: Optional[Pattern] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Compile the regex pattern after initialization."""
        try:
            self.compiled_pattern = re.compile(self.pattern, re.MULTILINE | re.IGNORECASE)
        except re.error as e:
            logger.error(f"Failed to compile pattern for rule {self.id}: {e}")
            self.compiled_pattern = None


@dataclass
class Finding:
    """A security finding from applying a rule."""
    rule_id: str
    rule_name: str
    severity: Severity
    file_path: str
    line_number: int
    line_content: str
    description: str
    remediation: str
    code_example: str
    owasp_category: str
    cwe_id: Optional[str] = None
    effort_minutes: int = 30


class RuleEngine:
    """
    Security rule engine for detecting vulnerabilities.
    
    This engine applies security rules to source code files and generates findings.
    """

    def __init__(self, rules: List[SecurityRule]):
        """
        Initialize the rule engine with a list of rules.
        
        Args:
            rules: List of SecurityRule objects to apply
        """
        self.rules = rules
        self.findings: List[Finding] = []
        logger.info(f"Initialized RuleEngine with {len(rules)} rules")

    def scan_file(self, file_path: Path, language: str) -> List[Finding]:
        """
        Scan a single file for security vulnerabilities.
        
        Args:
            file_path: Path to the file to scan
            language: Programming language of the file
            
        Returns:
            List of Finding objects
        """
        findings = []
        
        # Filter rules applicable to this language
        applicable_rules = [
            rule for rule in self.rules
            if language.lower() in [lang.lower() for lang in rule.languages]
        ]
        
        if not applicable_rules:
            return findings
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            for rule in applicable_rules:
                if rule.compiled_pattern is None:
                    continue
                
                # Search for pattern matches
                for line_num, line in enumerate(lines, start=1):
                    if rule.compiled_pattern.search(line):
                        finding = Finding(
                            rule_id=rule.id,
                            rule_name=rule.name,
                            severity=rule.severity,
                            file_path=str(file_path),
                            line_number=line_num,
                            line_content=line.strip(),
                            description=rule.description,
                            remediation=rule.remediation,
                            code_example=rule.code_example,
                            owasp_category=rule.owasp_category,
                            cwe_id=rule.cwe_id,
                            effort_minutes=rule.effort_minutes,
                        )
                        findings.append(finding)
                        
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")

        # Store findings for later retrieval
        self.findings.extend(findings)
        return findings

    def scan_directory(self, directory: Path, language_map: Dict[str, str]) -> List[Finding]:
        """
        Scan a directory for security vulnerabilities.
        
        Args:
            directory: Path to the directory to scan
            language_map: Mapping of file paths to languages
            
        Returns:
            List of Finding objects
        """
        all_findings = []
        
        for file_path_str, language in language_map.items():
            file_path = Path(file_path_str)
            if file_path.exists() and file_path.is_file():
                findings = self.scan_file(file_path, language)
                all_findings.extend(findings)
        
        self.findings = all_findings
        logger.info(f"Scan complete: {len(all_findings)} findings")
        return all_findings

    def get_findings_by_severity(self) -> Dict[Severity, List[Finding]]:
        """Group findings by severity level."""
        grouped = {severity: [] for severity in Severity}
        for finding in self.findings:
            grouped[finding.severity].append(finding)
        return grouped

    def get_critical_findings(self) -> List[Finding]:
        """Get only critical severity findings."""
        return [f for f in self.findings if f.severity == Severity.CRITICAL]

    def get_high_findings(self) -> List[Finding]:
        """Get only high severity findings."""
        return [f for f in self.findings if f.severity == Severity.HIGH]

