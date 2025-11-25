"""JSON exporter for analysis results."""

import json
from typing import Dict, Any, List
from pathlib import Path
from ..models import CodeAnalysis, Issue


class JSONExporter:
    """Export analysis results to JSON format."""

    def export(self, analysis: CodeAnalysis, output_path: str) -> None:
        """Export analysis to JSON file.

        Args:
            analysis: Code analysis results
            output_path: Path to output JSON file
        """
        data = self.to_dict(analysis)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def to_dict(self, analysis: CodeAnalysis) -> Dict[str, Any]:
        """Convert analysis to dictionary.

        Args:
            analysis: Code analysis results

        Returns:
            Dictionary representation
        """
        return {
            "version": "1.0.0",
            "structure": self._structure_to_dict(analysis.structure)
            if analysis.structure
            else None,
            "dependencies": [self._dependency_to_dict(d) for d in analysis.dependencies]
            if analysis.dependencies
            else [],
            "complexity_metrics": analysis.complexity_metrics
            if analysis.complexity_metrics
            else {},
            "quality_issues": [self._issue_to_dict(i) for i in analysis.quality_issues]
            if analysis.quality_issues
            else [],
            "summary": {
                "total_files": sum(
                    lang.file_count for lang in analysis.structure.languages
                )
                if analysis.structure and analysis.structure.languages
                else 0,
                "total_languages": len(analysis.structure.languages)
                if analysis.structure and analysis.structure.languages
                else 0,
                "total_dependencies": len(analysis.dependencies)
                if analysis.dependencies
                else 0,
                "total_issues": len(analysis.quality_issues)
                if analysis.quality_issues
                else 0,
                "critical_issues": len(
                    [
                        i
                        for i in analysis.quality_issues
                        if i.severity.value == "critical"
                    ]
                )
                if analysis.quality_issues
                else 0,
                "high_issues": len(
                    [i for i in analysis.quality_issues if i.severity.value == "high"]
                )
                if analysis.quality_issues
                else 0,
            },
        }

    def _structure_to_dict(self, structure) -> Dict[str, Any]:
        """Convert structure to dictionary."""
        return {
            "languages": [
                {
                    "name": lang.name,
                    "file_count": lang.file_count,
                    "line_count": lang.line_count,
                    "percentage": lang.percentage,
                }
                for lang in structure.languages
            ]
            if structure.languages
            else [],
            "frameworks": [
                {
                    "name": fw.name,
                    "version": fw.version if hasattr(fw, "version") else None,
                }
                for fw in structure.frameworks
            ]
            if structure.frameworks
            else [],
        }

    def _dependency_to_dict(self, dep) -> Dict[str, Any]:
        """Convert dependency to dictionary."""
        return {
            "name": dep.name,
            "type": dep.dependency_type,
            "version": dep.version,
            "source_file": dep.source_file,
        }

    def _issue_to_dict(self, issue: Issue) -> Dict[str, Any]:
        """Convert issue to dictionary."""
        return {
            "title": issue.title,
            "description": issue.description,
            "severity": issue.severity.value,
            "source": issue.source,
        }

    def to_json_string(self, analysis: CodeAnalysis) -> str:
        """Convert analysis to JSON string.

        Args:
            analysis: Code analysis results

        Returns:
            JSON string
        """
        data = self.to_dict(analysis)
        return json.dumps(data, indent=2, ensure_ascii=False)
