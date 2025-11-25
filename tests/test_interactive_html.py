"""Tests for interactive HTML exporter."""

from pathlib import Path

import pytest

from codebase_reviewer.exporters.interactive_html_exporter import InteractiveHTMLExporter
from codebase_reviewer.models import CodeAnalysis, Issue, Severity


class TestInteractiveHTMLExporter:
    """Tests for InteractiveHTMLExporter."""

    def test_initialization(self):
        """Test interactive HTML exporter initialization."""
        exporter = InteractiveHTMLExporter()
        assert exporter is not None

    def test_export_to_file(self, tmp_path):
        """Test exporting to HTML file."""
        exporter = InteractiveHTMLExporter()

        # Create sample analysis
        analysis = CodeAnalysis(
            quality_issues=[
                Issue(
                    title="SEC-001",
                    description="SQL injection vulnerability",
                    severity=Severity.CRITICAL,
                    source="test.py:10",
                ),
                Issue(
                    title="QUAL-001",
                    description="TODO comment found",
                    severity=Severity.LOW,
                    source="main.py:5",
                ),
            ]
        )

        output_path = tmp_path / "report.html"
        exporter.export(analysis, str(output_path))

        assert output_path.exists()

        # Check content
        content = output_path.read_text()
        assert "Interactive Code Analysis Report" in content
        assert "SQL injection" in content
        assert "TODO comment" in content

    def test_to_html_with_issues(self):
        """Test HTML generation with issues."""
        exporter = InteractiveHTMLExporter()

        analysis = CodeAnalysis(
            quality_issues=[
                Issue(
                    title="SEC-001",
                    description="Critical issue",
                    severity=Severity.CRITICAL,
                    source="test.py:10",
                ),
                Issue(
                    title="SEC-002",
                    description="High severity issue",
                    severity=Severity.HIGH,
                    source="test.py:20",
                ),
                Issue(
                    title="QUAL-001",
                    description="Medium issue",
                    severity=Severity.MEDIUM,
                    source="main.py:5",
                ),
            ]
        )

        html = exporter.to_html(analysis)

        assert "Interactive Code Analysis Report" in html
        assert "Total Issues" in html
        assert "Critical" in html
        assert "High" in html
        assert "Medium" in html
        assert "Security" in html
        assert "Quality" in html

        # Check for JavaScript functionality
        assert "renderIssues" in html
        assert "filter-btn" in html
        assert "search-box" in html

    def test_to_html_empty_issues(self):
        """Test HTML generation with no issues."""
        exporter = InteractiveHTMLExporter()

        analysis = CodeAnalysis(quality_issues=[])

        html = exporter.to_html(analysis)

        assert "Interactive Code Analysis Report" in html
        assert "Total Issues" in html

    def test_html_contains_filters(self):
        """Test that HTML contains filter buttons."""
        exporter = InteractiveHTMLExporter()

        analysis = CodeAnalysis(
            quality_issues=[
                Issue(
                    title="SEC-001",
                    description="Test issue",
                    severity=Severity.CRITICAL,
                    source="test.py:10",
                ),
            ]
        )

        html = exporter.to_html(analysis)

        # Check for filter buttons
        assert "All Issues" in html
        assert "Critical" in html
        assert "High" in html
        assert "Medium" in html
        assert "Low" in html
        assert "Security" in html
        assert "Quality" in html

    def test_html_contains_search(self):
        """Test that HTML contains search functionality."""
        exporter = InteractiveHTMLExporter()

        analysis = CodeAnalysis(quality_issues=[])

        html = exporter.to_html(analysis)

        # Check for search box
        assert "search-box" in html
        assert "searchBox" in html
        assert "Search by file name" in html
