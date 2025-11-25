"""Tests for visualization generators."""

import pytest

from codebase_reviewer.models import CodeAnalysis, CodeStructure, DependencyInfo, Framework, Issue, Language, Severity
from codebase_reviewer.visualization.chart_generator import ChartGenerator
from codebase_reviewer.visualization.mermaid_generator import MermaidGenerator


class TestMermaidGenerator:
    """Test Mermaid diagram generation."""

    def test_generate_architecture_diagram(self):
        """Test architecture diagram generation."""
        gen = MermaidGenerator()

        # Create test analysis
        structure = CodeStructure(
            languages=[
                Language(name="Python", file_count=10, percentage=60.0, line_count=1000),
                Language(name="JavaScript", file_count=5, percentage=30.0, line_count=500),
            ],
            frameworks=[Framework(name="Flask")],
        )
        analysis = CodeAnalysis(
            structure=structure,
            dependencies=[],
            complexity_metrics={},
            quality_issues=[],
        )

        diagram = gen.generate_architecture_diagram(analysis)
        assert "```mermaid" in diagram
        assert "graph TD" in diagram
        assert "Python" in diagram or "Flask" in diagram

    def test_generate_dependency_graph(self):
        """Test dependency graph generation."""
        gen = MermaidGenerator()

        dependencies = [
            DependencyInfo(name="flask", dependency_type="production", version="2.0.0"),
            DependencyInfo(name="pytest", dependency_type="development", version="7.0.0"),
        ]

        diagram = gen.generate_dependency_graph(dependencies)
        assert "```mermaid" in diagram
        assert "graph LR" in diagram
        assert "flask" in diagram or "pytest" in diagram

    def test_generate_data_flow_diagram(self):
        """Test data flow diagram generation."""
        gen = MermaidGenerator()

        analysis = CodeAnalysis(
            structure=None,
            dependencies=[],
            complexity_metrics={},
            quality_issues=[],
        )

        diagram = gen.generate_data_flow_diagram(analysis)
        assert "```mermaid" in diagram
        assert "flowchart TD" in diagram

    def test_generate_sequence_diagram(self):
        """Test sequence diagram generation."""
        gen = MermaidGenerator()

        diagram = gen.generate_sequence_diagram("Test Workflow")
        assert "```mermaid" in diagram
        assert "sequenceDiagram" in diagram


class TestChartGenerator:
    """Test chart and table generation."""

    def test_generate_language_distribution_table(self):
        """Test language distribution table."""
        gen = ChartGenerator()

        structure = CodeStructure(
            languages=[
                Language(name="Python", file_count=10, percentage=60.0, line_count=1000),
                Language(name="JavaScript", file_count=5, percentage=30.0, line_count=500),
            ],
            frameworks=[],
        )
        analysis = CodeAnalysis(
            structure=structure,
            dependencies=[],
            complexity_metrics={},
            quality_issues=[],
        )

        table = gen.generate_language_distribution_table(analysis)
        assert "| Language | Files | Percentage |" in table
        assert "Python" in table
        assert "JavaScript" in table

    def test_generate_issue_severity_table(self):
        """Test issue severity table."""
        gen = ChartGenerator()

        issues = [
            Issue(
                title="Critical Issue",
                description="Test",
                severity=Severity.CRITICAL,
                source="test.py",
            ),
            Issue(
                title="High Issue",
                description="Test",
                severity=Severity.HIGH,
                source="test.py",
            ),
            Issue(
                title="Low Issue",
                description="Test",
                severity=Severity.LOW,
                source="test.py",
            ),
        ]

        table = gen.generate_issue_severity_table(issues)
        assert "| Severity | Count | Percentage |" in table
        assert "Critical" in table
        assert "High" in table

    def test_generate_metrics_table(self):
        """Test metrics table."""
        gen = ChartGenerator()

        structure = CodeStructure(
            languages=[Language(name="Python", file_count=10, percentage=100.0, line_count=1000)],
            frameworks=[],
        )
        analysis = CodeAnalysis(
            structure=structure,
            dependencies=[],
            complexity_metrics={"average_complexity": 5.2},
            quality_issues=[],
        )

        table = gen.generate_metrics_table(analysis)
        assert "| Metric | Value |" in table
        assert "Total Files" in table

    def test_generate_framework_table(self):
        """Test framework table."""
        gen = ChartGenerator()

        structure = CodeStructure(
            languages=[],
            frameworks=[
                Framework(name="Flask"),
                Framework(name="pytest"),
            ],
        )
        analysis = CodeAnalysis(
            structure=structure,
            dependencies=[],
            complexity_metrics={},
            quality_issues=[],
        )

        table = gen.generate_framework_table(analysis)
        assert "| Framework | Version | Purpose |" in table
        assert "Flask" in table

    def test_generate_top_issues_table(self):
        """Test top issues table."""
        gen = ChartGenerator()

        issues = [
            Issue(
                title="Issue 1",
                description="Test",
                severity=Severity.CRITICAL,
                source="test.py:1",
            ),
            Issue(
                title="Issue 2",
                description="Test",
                severity=Severity.HIGH,
                source="test.py:2",
            ),
        ]

        table = gen.generate_top_issues_table(issues, limit=5)
        assert "| Severity | Issue | Location |" in table
        assert "Issue 1" in table
