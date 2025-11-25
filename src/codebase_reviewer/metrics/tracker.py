"""Metrics tracker for v2.0 obsolescence detection."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from codebase_reviewer.models_v2 import (
    ChangeMetrics,
    CoverageMetrics,
    Metrics,
    PatternMetrics,
    PerformanceMetrics,
    QualityMetrics,
    StalenessMetrics,
    TestMetrics,
    UserFeedbackMetrics,
)


class MetricsTracker:
    """Tracks metrics for obsolescence detection."""

    def __init__(self, codebase_path: Path, output_dir: Optional[Path] = None):
        """Initialize tracker.

        Args:
            codebase_path: Path to codebase being analyzed
            output_dir: Directory for metrics output (default: /tmp/codebase-reviewer/{name}/)
        """
        self.codebase_path = Path(codebase_path)

        if output_dir is None:
            codebase_name = self.codebase_path.name
            output_dir = Path(f"/tmp/codebase-reviewer/{codebase_name}")

        self.output_dir = Path(output_dir)
        self.metrics_file = self.output_dir / "metrics.json"

        self.metrics = Metrics()
        self.previous_metrics: Optional[Metrics] = None

    def load_previous_metrics(self) -> Optional[Metrics]:
        """Load metrics from previous run.

        Returns:
            Previous Metrics or None if no previous run
        """
        if not self.metrics_file.exists():
            return None

        try:
            with open(self.metrics_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            return Metrics(
                coverage=CoverageMetrics(**data.get("coverage", {})),
                changes=ChangeMetrics(**data.get("changes", {})),
                quality=QualityMetrics(**data.get("quality", {})),
                performance=PerformanceMetrics(**data.get("performance", {})),
                staleness=StalenessMetrics(**data.get("staleness", {})),
                patterns=PatternMetrics(**data.get("patterns", {})),
                tests=TestMetrics(**data.get("tests", {})),
                user_feedback=UserFeedbackMetrics(**data.get("user_feedback", {})),
            )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Warning: Failed to load previous metrics: {e}")
            return None

    def update_coverage(self, files_total: int, files_analyzed: int, files_documented: int) -> None:
        """Update coverage metrics.

        Args:
            files_total: Total files in codebase
            files_analyzed: Files successfully analyzed
            files_documented: Files with documentation generated
        """
        self.metrics.coverage.files_total = files_total
        self.metrics.coverage.files_analyzed = files_analyzed
        self.metrics.coverage.files_documented = files_documented

        if files_total > 0:
            self.metrics.coverage.coverage_percent = (files_analyzed / files_total) * 100

    def update_changes(
        self, files_changed: int, files_added: int, files_deleted: int, new_languages: List[str]
    ) -> None:
        """Update change detection metrics.

        Args:
            files_changed: Number of files changed since last run
            files_added: Number of files added
            files_deleted: Number of files deleted
            new_languages: List of newly detected languages
        """
        self.metrics.changes.files_changed = files_changed
        self.metrics.changes.files_added = files_added
        self.metrics.changes.files_deleted = files_deleted
        self.metrics.changes.new_languages = new_languages

        if self.metrics.coverage.files_total > 0:
            self.metrics.changes.files_changed_percent = (files_changed / self.metrics.coverage.files_total) * 100

    def update_quality(self, error_count: int, warning_count: int, false_positive_estimate: int) -> None:
        """Update quality metrics.

        Args:
            error_count: Number of errors detected
            warning_count: Number of warnings
            false_positive_estimate: Estimated false positives
        """
        self.metrics.quality.error_count = error_count
        self.metrics.quality.warning_count = warning_count
        self.metrics.quality.false_positive_estimate = false_positive_estimate

        total_findings = error_count + warning_count
        if total_findings > 0:
            self.metrics.quality.error_rate_percent = (error_count / total_findings) * 100

    def update_performance(self, runtime_seconds: float, memory_mb: float) -> None:
        """Update performance metrics.

        Args:
            runtime_seconds: Runtime in seconds
            memory_mb: Peak memory usage in MB
        """
        self.metrics.performance.avg_runtime_seconds = runtime_seconds
        self.metrics.performance.memory_usage_mb = memory_mb

    def update_staleness(self) -> None:
        """Update staleness metrics based on current time."""
        now = datetime.now()
        self.metrics.staleness.last_run_date = now.isoformat()

        # Calculate days since last run
        if self.previous_metrics and self.previous_metrics.staleness.last_run_date:
            try:
                last_run = datetime.fromisoformat(self.previous_metrics.staleness.last_run_date)
                delta = now - last_run
                self.metrics.staleness.days_since_last_run = delta.days
            except (ValueError, TypeError):
                self.metrics.staleness.days_since_last_run = 0
        else:
            self.metrics.staleness.days_since_last_run = 0

    def update_patterns(self, detected: List[str], newly_detected: List[str]) -> None:
        """Update pattern detection metrics.

        Args:
            detected: All detected patterns
            newly_detected: Patterns detected for first time
        """
        self.metrics.patterns.detected = detected
        self.metrics.patterns.newly_detected = newly_detected

    def update_tests(self, pass_count: int, fail_count: int) -> None:
        """Update test metrics.

        Args:
            pass_count: Number of passing regression tests
            fail_count: Number of failing regression tests
        """
        self.metrics.tests.regression_pass_count = pass_count
        self.metrics.tests.regression_fail_count = fail_count

    def add_user_feedback(self, override_flag: str, note: str = "") -> None:
        """Add user feedback.

        Args:
            override_flag: Human override flag
            note: Optional note
        """
        if override_flag not in self.metrics.user_feedback.human_override_flags:
            self.metrics.user_feedback.human_override_flags.append(override_flag)

        if note:
            if self.metrics.user_feedback.notes:
                self.metrics.user_feedback.notes += f"\n{note}"
            else:
                self.metrics.user_feedback.notes = note

    def save(self) -> None:
        """Save metrics to file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "coverage": {
                "files_total": self.metrics.coverage.files_total,
                "files_analyzed": self.metrics.coverage.files_analyzed,
                "files_documented": self.metrics.coverage.files_documented,
                "coverage_percent": self.metrics.coverage.coverage_percent,
            },
            "changes": {
                "files_changed": self.metrics.changes.files_changed,
                "files_changed_percent": self.metrics.changes.files_changed_percent,
                "files_added": self.metrics.changes.files_added,
                "files_deleted": self.metrics.changes.files_deleted,
                "new_languages": self.metrics.changes.new_languages,
            },
            "quality": {
                "error_count": self.metrics.quality.error_count,
                "error_rate_percent": self.metrics.quality.error_rate_percent,
                "warning_count": self.metrics.quality.warning_count,
                "false_positive_estimate": self.metrics.quality.false_positive_estimate,
            },
            "performance": {
                "avg_runtime_seconds": self.metrics.performance.avg_runtime_seconds,
                "memory_usage_mb": self.metrics.performance.memory_usage_mb,
            },
            "staleness": {
                "last_run_date": self.metrics.staleness.last_run_date,
                "days_since_last_run": self.metrics.staleness.days_since_last_run,
            },
            "patterns": {
                "detected": self.metrics.patterns.detected,
                "newly_detected": self.metrics.patterns.newly_detected,
            },
            "tests": {
                "regression_pass_count": self.metrics.tests.regression_pass_count,
                "regression_fail_count": self.metrics.tests.regression_fail_count,
            },
            "user_feedback": {
                "human_override_flags": self.metrics.user_feedback.human_override_flags,
                "notes": self.metrics.user_feedback.notes,
            },
        }

        with open(self.metrics_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_metrics(self) -> Metrics:
        """Get current metrics.

        Returns:
            Current Metrics object
        """
        return self.metrics
