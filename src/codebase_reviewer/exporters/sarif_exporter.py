"""SARIF exporter for GitHub Code Scanning integration."""

import json
from typing import Dict, Any, List
from pathlib import Path
from ..models import CodeAnalysis, Issue, Severity


class SARIFExporter:
    """Export analysis results to SARIF format (Static Analysis Results Interchange Format).
    
    SARIF is the standard format for GitHub Code Scanning and other security tools.
    Spec: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html
    """

    def export(self, analysis: CodeAnalysis, output_path: str, repository_root: str = ".") -> None:
        """Export analysis to SARIF file.

        Args:
            analysis: Code analysis results
            output_path: Path to output SARIF file
            repository_root: Root path of the repository
        """
        data = self.to_sarif(analysis, repository_root)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def to_sarif(self, analysis: CodeAnalysis, repository_root: str = ".") -> Dict[str, Any]:
        """Convert analysis to SARIF format.

        Args:
            analysis: Code analysis results
            repository_root: Root path of the repository

        Returns:
            SARIF dictionary
        """
        issues = analysis.quality_issues if analysis.quality_issues else []
        
        return {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "Codebase Reviewer",
                            "version": "1.0.0",
                            "informationUri": "https://github.com/bordenet/codebase-reviewer",
                            "rules": self._generate_rules(issues),
                        }
                    },
                    "results": self._generate_results(issues, repository_root),
                }
            ]
        }

    def _generate_rules(self, issues: List[Issue]) -> List[Dict[str, Any]]:
        """Generate SARIF rules from issues.

        Args:
            issues: List of issues

        Returns:
            List of SARIF rules
        """
        # Extract unique rule IDs from issue titles
        rules_map = {}
        for issue in issues:
            rule_id = self._issue_to_rule_id(issue)
            if rule_id not in rules_map:
                rules_map[rule_id] = {
                    "id": rule_id,
                    "name": issue.title,
                    "shortDescription": {
                        "text": issue.title
                    },
                    "fullDescription": {
                        "text": issue.description.split('\n')[0] if issue.description else issue.title
                    },
                    "defaultConfiguration": {
                        "level": self._severity_to_sarif_level(issue.severity)
                    },
                    "properties": {
                        "tags": ["security", "quality"],
                        "precision": "high"
                    }
                }
        
        return list(rules_map.values())

    def _generate_results(self, issues: List[Issue], repository_root: str) -> List[Dict[str, Any]]:
        """Generate SARIF results from issues.

        Args:
            issues: List of issues
            repository_root: Root path of the repository

        Returns:
            List of SARIF results
        """
        results = []
        for issue in issues:
            # Parse source location (format: "file.py:line" or just "file.py")
            source_parts = issue.source.split(':')
            file_path = source_parts[0]
            line_number = int(source_parts[1]) if len(source_parts) > 1 and source_parts[1].isdigit() else 1
            
            results.append({
                "ruleId": self._issue_to_rule_id(issue),
                "level": self._severity_to_sarif_level(issue.severity),
                "message": {
                    "text": issue.description
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": file_path,
                                "uriBaseId": "%SRCROOT%"
                            },
                            "region": {
                                "startLine": line_number,
                                "startColumn": 1
                            }
                        }
                    }
                ]
            })
        
        return results

    def _issue_to_rule_id(self, issue: Issue) -> str:
        """Convert issue to rule ID.

        Args:
            issue: Issue

        Returns:
            Rule ID
        """
        # Create a simple rule ID from the title
        rule_id = issue.title.lower().replace(' ', '-').replace('_', '-')
        # Remove special characters
        rule_id = ''.join(c for c in rule_id if c.isalnum() or c == '-')
        return rule_id[:50]  # Limit length

    def _severity_to_sarif_level(self, severity: Severity) -> str:
        """Convert severity to SARIF level.

        Args:
            severity: Severity enum

        Returns:
            SARIF level string
        """
        mapping = {
            Severity.CRITICAL: "error",
            Severity.HIGH: "error",
            Severity.MEDIUM: "warning",
            Severity.LOW: "note",
            Severity.INFO: "note",
        }
        return mapping.get(severity, "warning")

