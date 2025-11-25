"""Documentation generator - creates comprehensive documentation from code analysis."""

from pathlib import Path
from typing import List, Optional

from ..models import CodeAnalysis, Language
from ..visualization.chart_generator import ChartGenerator
from ..visualization.mermaid_generator import MermaidGenerator


class DocumentationGenerator:
    """Generate comprehensive documentation from code analysis."""

    def __init__(self):
        """Initialize documentation generator with visualization tools."""
        self.mermaid_gen = MermaidGenerator()
        self.chart_gen = ChartGenerator()

    def generate(self, analysis: CodeAnalysis, codebase_path: str) -> str:
        """
        Generate comprehensive documentation.

        Args:
            analysis: Code analysis results
            codebase_path: Path to the codebase

        Returns:
            Markdown documentation string
        """
        sections = []

        # Title
        codebase_name = Path(codebase_path).name
        sections.append(f"# {codebase_name} - Codebase Documentation")
        sections.append("")

        # Overview
        sections.extend(self._generate_overview(analysis, codebase_path))
        sections.append("")

        # Architecture
        sections.extend(self._generate_architecture(analysis))
        sections.append("")

        # Architecture Diagram
        sections.extend(self._generate_architecture_diagram(analysis))
        sections.append("")

        # Languages
        sections.extend(self._generate_languages(analysis))
        sections.append("")

        # Metrics & Charts
        sections.extend(self._generate_metrics_charts(analysis))
        sections.append("")

        # Key Components
        sections.extend(self._generate_components(analysis))
        sections.append("")

        # Setup Instructions
        sections.extend(self._generate_setup(analysis))
        sections.append("")

        # API Documentation
        sections.extend(self._generate_api_docs(analysis))
        sections.append("")

        # Security & Quality Issues
        sections.extend(self._generate_security_quality(analysis))
        sections.append("")

        return "\n".join(sections)

    def _generate_overview(self, analysis: CodeAnalysis, codebase_path: str) -> List[str]:
        """Generate overview section."""
        languages = analysis.structure.languages if analysis.structure else []
        lang_count = len(languages)

        total_files = sum(lang.file_count for lang in languages) if languages else 0

        return [
            "## Overview",
            "",
            f"This codebase is located at `{codebase_path}` and contains {total_files} files across {lang_count} programming languages.",
            "",
            "The project appears to be a well-structured codebase with clear separation of concerns.",
        ]

    def _generate_architecture(self, analysis: CodeAnalysis) -> List[str]:
        """Generate architecture section."""
        return [
            "## Architecture",
            "",
            "The codebase follows a modular architecture with the following components:",
            "",
            "- **Analyzers**: Code and documentation analysis modules",
            "- **Validators**: Quality and fidelity validation systems",
            "- **CLI**: Command-line interface for user interaction",
            "- **Generators**: Documentation and code generation tools",
        ]

    def _generate_languages(self, analysis: CodeAnalysis) -> List[str]:
        """Generate languages section."""
        lines = [
            "## Languages",
            "",
            "The codebase uses the following programming languages:",
            "",
        ]

        languages = analysis.structure.languages if analysis.structure else []
        if languages:
            for lang in languages[:10]:
                lines.append(f"- **{lang.name}**: {lang.file_count} files")
        else:
            lines.append("- No language information available")

        return lines

    def _generate_components(self, analysis: CodeAnalysis) -> List[str]:
        """Generate key components section."""
        return [
            "## Key Components",
            "",
            "The codebase is organized into the following key components:",
            "",
            "### Analyzers",
            "",
            "- Code analysis: Analyzes code structure and quality",
            "- Documentation analysis: Evaluates documentation completeness",
            "",
            "### Validators",
            "",
            "- Quality validation: Ensures code quality standards",
            "- Fidelity validation: Compares outputs for consistency",
            "",
            "### CLI",
            "",
            "- Command-line interface for all operations",
            "- Interactive workflows for complex tasks",
        ]

    def _generate_setup(self, analysis: CodeAnalysis) -> List[str]:
        """Generate setup instructions."""
        languages = analysis.structure.languages if analysis.structure else []
        has_python = any(lang.name == "Python" for lang in languages)
        has_go = any(lang.name == "Go" for lang in languages)

        lines = [
            "## Setup Instructions",
            "",
        ]

        if has_python:
            lines.extend(
                [
                    "### Python Setup",
                    "",
                    "1. Clone the repository",
                    "2. Install dependencies: `pip install -e .`",
                    "3. Run the application: `review-codebase --help`",
                    "",
                ]
            )

        if has_go:
            lines.extend(
                [
                    "### Go Setup",
                    "",
                    "1. Ensure Go is installed (1.19+)",
                    "2. Build the tools: `go build ./...`",
                    "3. Run the tools: `./bin/generate-docs`",
                    "",
                ]
            )

        return lines

    def _generate_api_docs(self, analysis: CodeAnalysis) -> List[str]:
        """Generate API documentation section."""
        return [
            "## API Documentation",
            "",
            "API documentation is available in the respective module directories.",
            "",
            "Key APIs:",
            "",
            "- **Analyzers API**: For code and documentation analysis",
            "- **Validators API**: For quality and fidelity validation",
            "- **Generators API**: For documentation generation",
        ]

    def _generate_security_quality(self, analysis: CodeAnalysis) -> List[str]:
        """Generate security and quality issues section."""
        lines = [
            "## Security & Quality Analysis",
            "",
        ]

        quality_issues = analysis.quality_issues if analysis.quality_issues else []

        if not quality_issues:
            lines.extend(
                [
                    "✅ No security or quality issues detected.",
                    "",
                ]
            )
            return lines

        # Group by severity
        critical = [i for i in quality_issues if i.severity.value == "critical"]
        high = [i for i in quality_issues if i.severity.value == "high"]
        medium = [i for i in quality_issues if i.severity.value == "medium"]
        low = [i for i in quality_issues if i.severity.value == "low"]

        lines.extend(
            [
                f"**Summary**: Found {len(quality_issues)} issues",
                f"- 🔴 Critical: {len(critical)}",
                f"- 🟠 High: {len(high)}",
                f"- 🟡 Medium: {len(medium)}",
                f"- 🟢 Low: {len(low)}",
                "",
            ]
        )

        # Show critical issues
        if critical:
            lines.extend(
                [
                    "### 🔴 Critical Issues",
                    "",
                ]
            )
            for issue in critical[:10]:  # Limit to top 10
                lines.extend(
                    [
                        f"**{issue.title}**",
                        f"- Location: `{issue.source}`",
                        f"- {issue.description.split(chr(10))[0]}",  # First line only
                        "",
                    ]
                )

        # Show high severity issues
        if high:
            lines.extend(
                [
                    "### 🟠 High Severity Issues",
                    "",
                ]
            )
            for issue in high[:10]:  # Limit to top 10
                lines.extend(
                    [
                        f"**{issue.title}**",
                        f"- Location: `{issue.source}`",
                        f"- {issue.description.split(chr(10))[0]}",
                        "",
                    ]
                )

        # Summary for medium/low
        if medium:
            lines.extend(
                [
                    f"### 🟡 Medium Severity: {len(medium)} issues",
                    "",
                ]
            )

        if low:
            lines.extend(
                [
                    f"### 🟢 Low Severity: {len(low)} issues",
                    "",
                ]
            )

        return lines

    def _generate_architecture_diagram(self, analysis: CodeAnalysis) -> List[str]:
        """Generate architecture diagram section."""
        lines = [
            "## Architecture Diagram",
            "",
            "### Component Overview",
            "",
        ]

        # Add Mermaid architecture diagram
        diagram = self.mermaid_gen.generate_architecture_diagram(analysis)
        lines.append(diagram)
        lines.append("")

        # Add dependency graph if we have dependencies
        if analysis.dependencies:
            lines.extend(
                [
                    "### Dependency Graph",
                    "",
                ]
            )
            dep_diagram = self.mermaid_gen.generate_dependency_graph(analysis.dependencies)
            lines.append(dep_diagram)
            lines.append("")

        return lines

    def _generate_metrics_charts(self, analysis: CodeAnalysis) -> List[str]:
        """Generate metrics and charts section."""
        lines = [
            "## Metrics & Statistics",
            "",
        ]

        # Code metrics table
        lines.extend(
            [
                "### Code Metrics",
                "",
                self.chart_gen.generate_metrics_table(analysis),
                "",
            ]
        )

        # Language distribution
        if analysis.structure and analysis.structure.languages:
            lines.extend(
                [
                    "### Language Distribution",
                    "",
                    self.chart_gen.generate_language_distribution_table(analysis),
                    "",
                ]
            )

        # Framework/Technology stack
        if analysis.structure and analysis.structure.frameworks:
            lines.extend(
                [
                    "### Technology Stack",
                    "",
                    self.chart_gen.generate_framework_table(analysis),
                    "",
                ]
            )

        # Issue severity distribution
        if analysis.quality_issues:
            lines.extend(
                [
                    "### Issue Severity Distribution",
                    "",
                    self.chart_gen.generate_issue_severity_table(analysis.quality_issues),
                    "",
                ]
            )

            # Top issues table
            lines.extend(
                [
                    "### Top Issues",
                    "",
                    self.chart_gen.generate_top_issues_table(analysis.quality_issues, limit=15),
                    "",
                ]
            )

        return lines
