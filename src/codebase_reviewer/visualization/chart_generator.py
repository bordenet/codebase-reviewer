"""Chart generator for metrics visualization."""

from typing import Dict, List

from ..models import CodeAnalysis, Issue, Severity


class ChartGenerator:
    """Generate charts and tables from code analysis."""

    def generate_language_distribution_table(self, analysis: CodeAnalysis) -> str:
        """Generate language distribution table.

        Args:
            analysis: Code analysis results

        Returns:
            Markdown table as string
        """
        if not analysis.structure or not analysis.structure.languages:
            return "No language data available."

        lines = [
            "| Language | Files | Percentage |",
            "|----------|-------|------------|",
        ]

        for lang in analysis.structure.languages:
            lines.append(
                f"| {lang.name} | {lang.file_count} | {lang.percentage:.1f}% |"
            )

        return "\n".join(lines)

    def generate_issue_severity_table(self, issues: List[Issue]) -> str:
        """Generate issue severity distribution table.

        Args:
            issues: List of issues

        Returns:
            Markdown table as string
        """
        if not issues:
            return "No issues found."

        # Count by severity
        severity_counts = {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
        }

        for issue in issues:
            severity_name = issue.severity.value.capitalize()
            if severity_name in severity_counts:
                severity_counts[severity_name] += 1

        lines = [
            "| Severity | Count | Percentage |",
            "|----------|-------|------------|",
        ]

        total = len(issues)
        for severity, count in severity_counts.items():
            percentage = (count / total * 100) if total > 0 else 0
            emoji = self._get_severity_emoji(severity)
            lines.append(f"| {emoji} {severity} | {count} | {percentage:.1f}% |")

        return "\n".join(lines)

    def generate_metrics_table(self, analysis: CodeAnalysis) -> str:
        """Generate code metrics table.

        Args:
            analysis: Code analysis results

        Returns:
            Markdown table as string
        """
        lines = [
            "| Metric | Value |",
            "|--------|-------|",
        ]

        # Calculate metrics
        total_files = (
            sum(lang.file_count for lang in analysis.structure.languages)
            if analysis.structure and analysis.structure.languages
            else 0
        )
        total_languages = (
            len(analysis.structure.languages)
            if analysis.structure and analysis.structure.languages
            else 0
        )
        total_dependencies = len(analysis.dependencies) if analysis.dependencies else 0
        total_issues = len(analysis.quality_issues) if analysis.quality_issues else 0

        lines.extend(
            [
                f"| Total Files | {total_files} |",
                f"| Languages | {total_languages} |",
                f"| Dependencies | {total_dependencies} |",
                f"| Quality Issues | {total_issues} |",
            ]
        )

        # Add complexity metrics if available
        if analysis.complexity_metrics:
            for metric, value in analysis.complexity_metrics.items():
                lines.append(f"| {metric.replace('_', ' ').title()} | {value} |")

        return "\n".join(lines)

    def generate_framework_table(self, analysis: CodeAnalysis) -> str:
        """Generate framework/technology table.

        Args:
            analysis: Code analysis results

        Returns:
            Markdown table as string
        """
        if not analysis.structure or not analysis.structure.frameworks:
            return "No frameworks detected."

        lines = [
            "| Framework | Version | Purpose |",
            "|-----------|---------|---------|",
        ]

        for fw in analysis.structure.frameworks:
            version = fw.version if hasattr(fw, "version") and fw.version else "N/A"
            purpose = self._infer_framework_purpose(fw.name)
            lines.append(f"| {fw.name} | {version} | {purpose} |")

        return "\n".join(lines)

    def generate_top_issues_table(self, issues: List[Issue], limit: int = 10) -> str:
        """Generate table of top issues.

        Args:
            issues: List of issues
            limit: Maximum number of issues to show

        Returns:
            Markdown table as string
        """
        if not issues:
            return "No issues found."

        # Sort by severity (critical first)
        severity_order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
        }
        sorted_issues = sorted(
            issues, key=lambda i: severity_order.get(i.severity, 999)
        )

        lines = [
            "| Severity | Issue | Location |",
            "|----------|-------|----------|",
        ]

        for issue in sorted_issues[:limit]:
            emoji = self._get_severity_emoji(issue.severity.value.capitalize())
            title = issue.title[:50] + "..." if len(issue.title) > 50 else issue.title
            location = (
                issue.source[:40] + "..." if len(issue.source) > 40 else issue.source
            )
            lines.append(f"| {emoji} | {title} | `{location}` |")

        return "\n".join(lines)

    def _get_severity_emoji(self, severity: str) -> str:
        """Get emoji for severity level."""
        emoji_map = {
            "Critical": "🔴",
            "High": "🟠",
            "Medium": "🟡",
            "Low": "🟢",
        }
        return emoji_map.get(severity, "⚪")

    def _infer_framework_purpose(self, name: str) -> str:
        """Infer framework purpose from name."""
        name_lower = name.lower()
        if "test" in name_lower or "pytest" in name_lower:
            return "Testing"
        elif "flask" in name_lower or "django" in name_lower or "fastapi" in name_lower:
            return "Web Framework"
        elif "react" in name_lower or "vue" in name_lower or "angular" in name_lower:
            return "Frontend"
        elif "sql" in name_lower or "mongo" in name_lower or "redis" in name_lower:
            return "Database"
        else:
            return "Library"
