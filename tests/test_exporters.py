"""Tests for export modules."""

import json
import tempfile
from pathlib import Path
import pytest

from codebase_reviewer.exporters.json_exporter import JSONExporter
from codebase_reviewer.exporters.html_exporter import HTMLExporter
from codebase_reviewer.exporters.sarif_exporter import SARIFExporter
from codebase_reviewer.models import (
    CodeAnalysis,
    CodeStructure,
    Language,
    Framework,
    DependencyInfo,
    Issue,
    Severity,
)


@pytest.fixture
def sample_analysis():
    """Create sample analysis for testing."""
    structure = CodeStructure(
        languages=[
            Language(name="Python", file_count=10, percentage=60.0, line_count=1000),
            Language(name="JavaScript", file_count=5, percentage=30.0, line_count=500),
        ],
        frameworks=[Framework(name="Flask")],
    )

    issues = [
        Issue(
            title="Hardcoded Password",
            description="Password found in source code",
            severity=Severity.CRITICAL,
            source="app.py:42",
        ),
        Issue(
            title="TODO Comment",
            description="TODO: Fix this later",
            severity=Severity.LOW,
            source="utils.py:10",
        ),
    ]

    dependencies = [
        DependencyInfo(name="flask", dependency_type="production", version="2.0.0"),
        DependencyInfo(name="pytest", dependency_type="development", version="7.0.0"),
    ]

    return CodeAnalysis(
        structure=structure,
        dependencies=dependencies,
        complexity_metrics={"average_complexity": 5.2},
        quality_issues=issues,
    )


class TestJSONExporter:
    """Test JSON export functionality."""

    def test_export_to_file(self, sample_analysis, tmp_path):
        """Test exporting to JSON file."""
        exporter = JSONExporter()
        output_file = tmp_path / "analysis.json"

        exporter.export(sample_analysis, str(output_file))

        assert output_file.exists()

        # Verify JSON is valid
        with open(output_file) as f:
            data = json.load(f)

        assert data["version"] == "1.0.0"
        assert "structure" in data
        assert "quality_issues" in data

    def test_to_dict(self, sample_analysis):
        """Test converting analysis to dictionary."""
        exporter = JSONExporter()
        data = exporter.to_dict(sample_analysis)

        assert data["version"] == "1.0.0"
        assert len(data["structure"]["languages"]) == 2
        assert len(data["quality_issues"]) == 2
        assert data["summary"]["total_issues"] == 2
        assert data["summary"]["critical_issues"] == 1

    def test_to_json_string(self, sample_analysis):
        """Test converting to JSON string."""
        exporter = JSONExporter()
        json_str = exporter.to_json_string(sample_analysis)

        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data["version"] == "1.0.0"


class TestHTMLExporter:
    """Test HTML export functionality."""

    def test_export_to_file(self, sample_analysis, tmp_path):
        """Test exporting to HTML file."""
        exporter = HTMLExporter()
        output_file = tmp_path / "report.html"

        exporter.export(sample_analysis, str(output_file), title="Test Report")

        assert output_file.exists()

        # Verify HTML content
        with open(output_file) as f:
            html = f.read()

        assert "<!DOCTYPE html>" in html
        assert "Test Report" in html
        assert "Hardcoded Password" in html

    def test_to_html(self, sample_analysis):
        """Test converting to HTML."""
        exporter = HTMLExporter()
        html = exporter.to_html(sample_analysis, title="Test Report")

        assert "<!DOCTYPE html>" in html
        assert "Test Report" in html
        assert "Hardcoded Password" in html
        assert "severity-critical" in html
        assert "severity-low" in html

    def test_html_escaping(self, sample_analysis):
        """Test HTML special character escaping."""
        exporter = HTMLExporter()

        # Add issue with special characters
        sample_analysis.quality_issues.append(
            Issue(
                title="Test <script>alert('xss')</script>",
                description="Test & < > \" '",
                severity=Severity.HIGH,
                source="test.py:1",
            )
        )

        html = exporter.to_html(sample_analysis)

        # Verify escaping
        assert "&lt;script&gt;" in html
        assert "&amp;" in html
        assert "&quot;" in html or "&#39;" in html


class TestSARIFExporter:
    """Test SARIF export functionality."""

    def test_export_to_file(self, sample_analysis, tmp_path):
        """Test exporting to SARIF file."""
        exporter = SARIFExporter()
        output_file = tmp_path / "results.sarif"

        exporter.export(sample_analysis, str(output_file))

        assert output_file.exists()

        # Verify SARIF is valid JSON
        with open(output_file) as f:
            data = json.load(f)

        assert data["version"] == "2.1.0"
        assert "$schema" in data
        assert "runs" in data

    def test_to_sarif(self, sample_analysis):
        """Test converting to SARIF format."""
        exporter = SARIFExporter()
        sarif = exporter.to_sarif(sample_analysis)

        assert sarif["version"] == "2.1.0"
        assert len(sarif["runs"]) == 1

        run = sarif["runs"][0]
        assert run["tool"]["driver"]["name"] == "Codebase Reviewer"
        assert len(run["results"]) == 2
        assert len(run["tool"]["driver"]["rules"]) >= 1

    def test_severity_mapping(self, sample_analysis):
        """Test severity to SARIF level mapping."""
        exporter = SARIFExporter()

        assert exporter._severity_to_sarif_level(Severity.CRITICAL) == "error"
        assert exporter._severity_to_sarif_level(Severity.HIGH) == "error"
        assert exporter._severity_to_sarif_level(Severity.MEDIUM) == "warning"
        assert exporter._severity_to_sarif_level(Severity.LOW) == "note"

    def test_sarif_result_structure(self, sample_analysis):
        """Test SARIF result structure."""
        exporter = SARIFExporter()
        sarif = exporter.to_sarif(sample_analysis)

        result = sarif["runs"][0]["results"][0]

        assert "ruleId" in result
        assert "level" in result
        assert "message" in result
        assert "locations" in result
        assert len(result["locations"]) == 1

        location = result["locations"][0]
        assert "physicalLocation" in location
        assert "artifactLocation" in location["physicalLocation"]
        assert "region" in location["physicalLocation"]
