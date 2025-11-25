"""Basic tests for v2.0 architecture components to increase coverage."""

import tempfile
from pathlib import Path

import pytest

from codebase_reviewer.models_v2 import (
    CheckStatus,
    Confidence,
    Finding,
    FindingCategory,
    QualityGateStatus,
    RiskLevel,
    Severity,
)
from codebase_reviewer.prompts.generator_v2 import Phase1PromptGeneratorV2, ScanParameters
from codebase_reviewer.prompts.v2_loader import PromptTemplateV2Loader


class TestPromptTemplateV2Loader:
    """Test v2.0 prompt template loader."""

    def test_load_phase1_template(self):
        """Test loading Phase 1 template."""
        loader = PromptTemplateV2Loader()
        template = loader.load_phase1_template()

        assert template.version == "2.0"
        assert template.template_type == "phase1_codebase_analysis"
        assert len(template.tasks) > 0
        assert template.role is not None
        assert len(template.context) > 0


class TestPromptGeneratorV2:
    """Test v2.0 prompt generator."""

    def test_generate_phase1_prompt(self):
        """Test generating Phase 1 prompt."""
        generator = Phase1PromptGeneratorV2()
        params = ScanParameters(
            target_path="/test/repo", scan_mode="review", languages=["python", "go"], exclude_patterns=["*.test.py"]
        )
        prompt = generator.generate_prompt(params)

        assert "/test/repo" in prompt
        assert "review" in prompt.lower()
        assert len(prompt) > 500  # Should be substantial

    def test_scan_parameters_defaults(self):
        """Test ScanParameters default values."""
        params = ScanParameters(target_path="/test/repo")

        assert params.scan_mode == "review"
        assert params.output_path == "/tmp/codebase-reviewer"
        assert params.max_file_size_kb == 500


class TestModelsV2:
    """Test v2.0 data models."""

    def test_finding_model(self):
        """Test Finding model."""
        finding = Finding(
            id="SEC001",
            category=FindingCategory.SECURITY,
            severity=Severity.CRITICAL,
            confidence=Confidence.HIGH,
            description="Potential SQL injection vulnerability",
            remediation_summary="Use parameterized queries",
            file_path="app.py",
            line_number=42,
            cwe_id="CWE-89",
            owasp_category="A03:2021-Injection",
        )

        assert finding.severity == Severity.CRITICAL
        assert finding.confidence == Confidence.HIGH
        assert finding.cwe_id == "CWE-89"
        assert finding.category == FindingCategory.SECURITY

    def test_enums(self):
        """Test enum values."""
        assert Severity.CRITICAL.value == "Critical"
        assert Confidence.HIGH.value == "High"
        assert RiskLevel.HIGH.value == "High"
        assert QualityGateStatus.FAIL.value == "Fail"
        assert CheckStatus.PASS.value == "Pass"
        assert FindingCategory.SECURITY.value == "security"


class TestMetricsTracker:
    """Test metrics tracker."""

    def test_metrics_tracker_initialization(self):
        """Test metrics tracker initialization."""
        from codebase_reviewer.metrics.tracker import MetricsTracker

        with tempfile.TemporaryDirectory() as tmpdir:
            tracker = MetricsTracker(codebase_path=Path(tmpdir), output_dir=Path(tmpdir))

            assert tracker.codebase_path == Path(tmpdir)
            assert tracker.metrics is not None

    def test_update_coverage(self):
        """Test updating coverage metrics."""
        from codebase_reviewer.metrics.tracker import MetricsTracker

        with tempfile.TemporaryDirectory() as tmpdir:
            tracker = MetricsTracker(codebase_path=Path(tmpdir), output_dir=Path(tmpdir))
            tracker.update_coverage(files_total=100, files_analyzed=95, files_documented=80)

            assert tracker.metrics.coverage.files_total == 100
            assert tracker.metrics.coverage.files_analyzed == 95
            assert tracker.metrics.coverage.files_documented == 80


class TestObsolescenceDetector:
    """Test obsolescence detector."""

    def test_detector_initialization(self):
        """Test detector initialization."""
        from codebase_reviewer.obsolescence.detector import ObsolescenceDetector, ObsolescenceThresholds

        with tempfile.TemporaryDirectory() as tmpdir:
            detector = ObsolescenceDetector(codebase_path=Path(tmpdir))
            assert detector.thresholds.files_changed_percent == 30.0

    def test_custom_thresholds(self):
        """Test custom thresholds."""
        from codebase_reviewer.obsolescence.detector import ObsolescenceDetector, ObsolescenceThresholds

        with tempfile.TemporaryDirectory() as tmpdir:
            thresholds = ObsolescenceThresholds(files_changed_percent=50.0, stale_run_days_max=60)
            detector = ObsolescenceDetector(codebase_path=Path(tmpdir), thresholds=thresholds)

            assert detector.thresholds.files_changed_percent == 50.0
            assert detector.thresholds.stale_run_days_max == 60

