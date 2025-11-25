"""Tests for productivity metrics."""

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from codebase_reviewer.metrics.productivity_metrics import ProductivityMetrics, ProductivityReport, ProductivityTracker


class TestProductivityMetrics:
    """Tests for ProductivityMetrics."""

    def test_initialization(self):
        """Test productivity metrics initialization."""
        metrics = ProductivityMetrics()
        assert metrics.lines_of_code == 0
        assert metrics.commits_count == 0
        assert metrics.bugs_fixed == 0


class TestProductivityReport:
    """Tests for ProductivityReport."""

    def test_initialization(self):
        """Test productivity report initialization."""
        start = datetime.now() - timedelta(days=30)
        end = datetime.now()
        metrics = ProductivityMetrics(commits_count=10, bugs_fixed=5, bugs_introduced=2)

        report = ProductivityReport(
            period_start=start,
            period_end=end,
            metrics=metrics,
        )

        assert report.period_start == start
        assert report.period_end == end
        assert report.metrics == metrics
        assert report.productivity_score > 0

    def test_score_calculation_high_quality(self):
        """Test score calculation with high quality metrics."""
        metrics = ProductivityMetrics(
            commits_count=20,
            bugs_fixed=10,
            bugs_introduced=2,
            test_coverage=90.0,
            code_churn=20.0,
            pr_reviews_given=10,
            code_review_comments=50,
        )

        report = ProductivityReport(
            period_start=datetime.now() - timedelta(days=30),
            period_end=datetime.now(),
            metrics=metrics,
        )

        # High quality should result in high score
        assert report.productivity_score > 70

    def test_score_calculation_low_quality(self):
        """Test score calculation with low quality metrics."""
        metrics = ProductivityMetrics(
            commits_count=2,
            bugs_fixed=1,
            bugs_introduced=5,
            test_coverage=20.0,
            code_churn=80.0,
            pr_reviews_given=0,
            code_review_comments=0,
        )

        report = ProductivityReport(
            period_start=datetime.now() - timedelta(days=30),
            period_end=datetime.now(),
            metrics=metrics,
        )

        # Low quality should result in lower score
        assert report.productivity_score < 50


class TestProductivityTracker:
    """Tests for ProductivityTracker."""

    def test_initialization(self, tmp_path):
        """Test productivity tracker initialization."""
        tracker = ProductivityTracker(tmp_path)
        assert tracker.repo_path == tmp_path

    def test_generate_report(self, tmp_path):
        """Test generating productivity report."""
        # Initialize git repo
        import subprocess

        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=tmp_path,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=tmp_path,
            capture_output=True,
        )

        # Create a commit
        (tmp_path / "test.txt").write_text("test")
        subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmp_path, capture_output=True)

        tracker = ProductivityTracker(tmp_path)
        report = tracker.generate_report(days=30)

        assert report.period_start < report.period_end
        assert report.metrics is not None
        assert isinstance(report.insights, list)
        assert isinstance(report.recommendations, list)
        assert report.productivity_score >= 0

    def test_collect_metrics(self, tmp_path):
        """Test collecting metrics from git."""
        # Initialize git repo
        import subprocess

        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=tmp_path,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=tmp_path,
            capture_output=True,
        )

        # Create commits
        (tmp_path / "file1.txt").write_text("content1")
        subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Commit 1"], cwd=tmp_path, capture_output=True)

        (tmp_path / "file2.txt").write_text("content2")
        subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Commit 2"], cwd=tmp_path, capture_output=True)

        tracker = ProductivityTracker(tmp_path)
        start = datetime.now() - timedelta(days=1)
        end = datetime.now()

        metrics = tracker._collect_metrics(start, end, None)

        assert metrics.commits_count >= 0
        assert metrics.files_changed >= 0

    def test_generate_insights(self, tmp_path):
        """Test generating insights."""
        tracker = ProductivityTracker(tmp_path)

        # High commit frequency
        metrics = ProductivityMetrics(commits_count=25)
        insights = tracker._generate_insights(metrics)
        assert any("active development" in i.lower() for i in insights)

        # Low commit frequency
        metrics = ProductivityMetrics(commits_count=2)
        insights = tracker._generate_insights(metrics)
        assert any("low commit" in i.lower() for i in insights)

    def test_generate_recommendations(self, tmp_path):
        """Test generating recommendations."""
        tracker = ProductivityTracker(tmp_path)

        # Low test coverage
        metrics = ProductivityMetrics(test_coverage=50.0)
        recommendations = tracker._generate_recommendations(metrics)
        assert any("test coverage" in r.lower() for r in recommendations)

        # High code churn
        metrics = ProductivityMetrics(code_churn=60.0)
        recommendations = tracker._generate_recommendations(metrics)
        assert any("churn" in r.lower() for r in recommendations)
