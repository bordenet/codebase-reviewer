"""Tests for analytics module."""

import pytest
from datetime import datetime
from pathlib import Path
from codebase_reviewer.analytics.trend_analyzer import TrendAnalyzer, MetricSnapshot
from codebase_reviewer.analytics.hotspot_detector import HotspotDetector
from codebase_reviewer.analytics.risk_scorer import RiskScorer


class TestTrendAnalyzer:
    """Tests for TrendAnalyzer."""

    def test_initialization(self, tmp_path):
        """Test trend analyzer initialization."""
        history_file = tmp_path / "history.json"
        analyzer = TrendAnalyzer(history_file)
        assert analyzer.history_file == history_file
        assert analyzer.snapshots == []

    def test_record_snapshot(self, tmp_path):
        """Test recording a snapshot."""
        history_file = tmp_path / "history.json"
        analyzer = TrendAnalyzer(history_file)

        snapshot = MetricSnapshot(
            timestamp=datetime.now(),
            total_issues=10,
            critical_issues=2,
            high_issues=3,
            medium_issues=3,
            low_issues=2,
            total_files=50,
            total_lines=5000,
            security_issues=5,
            quality_issues=5,
        )

        analyzer.record_snapshot(snapshot)
        assert len(analyzer.snapshots) == 1
        assert analyzer.snapshots[0] == snapshot

    def test_get_trends_insufficient_data(self, tmp_path):
        """Test getting trends with insufficient data."""
        history_file = tmp_path / "history.json"
        analyzer = TrendAnalyzer(history_file)

        snapshot = MetricSnapshot(
            timestamp=datetime.now(),
            total_issues=10,
            critical_issues=2,
            high_issues=3,
            medium_issues=3,
            low_issues=2,
            total_files=50,
            total_lines=5000,
            security_issues=5,
            quality_issues=5,
        )

        analyzer.record_snapshot(snapshot)
        trends = analyzer.get_trends()
        assert trends == []

    def test_get_trends_improving(self, tmp_path):
        """Test getting trends when metrics are improving."""
        history_file = tmp_path / "history.json"
        analyzer = TrendAnalyzer(history_file)

        # Record first snapshot
        snapshot1 = MetricSnapshot(
            timestamp=datetime.now(),
            total_issues=20,
            critical_issues=5,
            high_issues=5,
            medium_issues=5,
            low_issues=5,
            total_files=50,
            total_lines=5000,
            security_issues=10,
            quality_issues=10,
        )
        analyzer.record_snapshot(snapshot1)

        # Record second snapshot with fewer issues
        snapshot2 = MetricSnapshot(
            timestamp=datetime.now(),
            total_issues=10,
            critical_issues=2,
            high_issues=3,
            medium_issues=3,
            low_issues=2,
            total_files=50,
            total_lines=5000,
            security_issues=5,
            quality_issues=5,
        )
        analyzer.record_snapshot(snapshot2)

        trends = analyzer.get_trends()
        assert len(trends) == 4

        # Check total issues trend
        total_trend = next(t for t in trends if t.metric_name == "total_issues")
        assert total_trend.current_value == 10
        assert total_trend.previous_value == 20
        assert total_trend.change == -10
        assert total_trend.direction == "improving"


class TestHotspotDetector:
    """Tests for HotspotDetector."""

    def test_initialization(self, tmp_path):
        """Test hotspot detector initialization."""
        detector = HotspotDetector(tmp_path)
        assert detector.repo_path == tmp_path

    def test_detect_hotspots_empty(self, tmp_path):
        """Test detecting hotspots with no issues."""
        detector = HotspotDetector(tmp_path)
        hotspots = detector.detect_hotspots({}, {})
        assert hotspots == []

    def test_detect_hotspots_with_issues(self, tmp_path):
        """Test detecting hotspots with issues."""
        detector = HotspotDetector(tmp_path)

        file_issues = {
            "file1.py": [
                {"severity": "high"},
                {"severity": "high"},
                {"severity": "medium"},
                {"severity": "medium"},
                {"severity": "low"},
            ]
        }

        file_metrics = {"file1.py": {"lines_of_code": 800}}

        hotspots = detector.detect_hotspots(file_issues, file_metrics)
        assert len(hotspots) >= 1
        assert hotspots[0].file_path == "file1.py"
        assert hotspots[0].bug_count == 5
        assert hotspots[0].risk_score > 3.0


class TestRiskScorer:
    """Tests for RiskScorer."""

    def test_initialization(self):
        """Test risk scorer initialization."""
        scorer = RiskScorer()
        assert scorer.severity_weights["critical"] == 10.0
        assert scorer.impact_weights["high"] == 7.0

    def test_score_issues_empty(self):
        """Test scoring with no issues."""
        scorer = RiskScorer()
        scores = scorer.score_issues([])
        assert scores == []

    def test_score_issues_critical(self):
        """Test scoring critical issues."""
        scorer = RiskScorer()

        issues = [
            {
                "id": "SEC-001",
                "severity": "critical",
                "file_path": "auth.py",
                "effort_minutes": 30,
            }
        ]

        scores = scorer.score_issues(issues)
        assert len(scores) == 1
        assert scores[0].severity == "critical"
        assert scores[0].priority == "critical"
        assert scores[0].risk_score > 10

    def test_score_issues_quick_win(self):
        """Test identifying quick wins."""
        scorer = RiskScorer()

        issues = [
            {
                "id": "SEC-002",
                "severity": "high",
                "file_path": "config.py",
                "effort_minutes": 15,
            }
        ]

        scores = scorer.score_issues(issues)
        assert len(scores) == 1
        assert scores[0].is_quick_win is True

    def test_score_issues_with_hotspots(self):
        """Test scoring with hotspot context."""
        scorer = RiskScorer()

        issues = [
            {
                "id": "QUAL-001",
                "severity": "medium",
                "file_path": "hotspot.py",
                "effort_minutes": 45,
            }
        ]

        hotspots = [{"file_path": "hotspot.py"}]

        scores = scorer.score_issues(issues, hotspots)
        assert len(scores) == 1
        assert scores[0].impact == "high"  # Elevated due to hotspot
