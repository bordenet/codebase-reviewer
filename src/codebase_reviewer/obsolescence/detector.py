"""Obsolescence detection logic for Phase 2 tools."""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from codebase_reviewer.models_v2 import Metrics


@dataclass
class ObsolescenceThresholds:
    """Thresholds for obsolescence detection."""

    files_changed_percent: float = 30.0
    new_languages_detected: bool = True
    coverage_min_percent: float = 85.0
    stale_run_days_max: int = 30
    error_rate_max_percent: float = 5.0
    regeneration_cooldown_days: int = 7


@dataclass
class ObsolescenceResult:
    """Result of obsolescence detection."""

    is_obsolete: bool
    reasons: List[str] = field(default_factory=list)
    metrics: Optional[Metrics] = None
    should_regenerate: bool = False
    suppressed: bool = False
    suppression_reason: str = ""


class ObsolescenceDetector:
    """Detects when Phase 2 tools have become obsolete."""

    def __init__(
        self,
        codebase_path: Path,
        metrics_file: Optional[Path] = None,
        thresholds: Optional[ObsolescenceThresholds] = None,
    ):
        """Initialize detector.

        Args:
            codebase_path: Path to the codebase being analyzed
            metrics_file: Path to metrics JSON file (default: /tmp/codebase-reviewer/{name}/metrics.json)
            thresholds: Custom thresholds (default: use defaults)
        """
        self.codebase_path = Path(codebase_path)
        self.thresholds = thresholds or ObsolescenceThresholds()

        if metrics_file is None:
            codebase_name = self.codebase_path.name
            metrics_file = Path(f"/tmp/codebase-reviewer/{codebase_name}/metrics.json")

        self.metrics_file = Path(metrics_file)
        self.previous_metrics: Optional[Metrics] = None
        self.current_metrics: Optional[Metrics] = None

    def load_previous_metrics(self) -> Optional[Metrics]:
        """Load metrics from previous run.

        Returns:
            Metrics object or None if no previous run
        """
        if not self.metrics_file.exists():
            return None

        try:
            with open(self.metrics_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Convert dict to Metrics object
            from codebase_reviewer.models_v2 import (
                ChangeMetrics,
                CoverageMetrics,
                PatternMetrics,
                PerformanceMetrics,
                QualityMetrics,
                StalenessMetrics,
                TestMetrics,
                UserFeedbackMetrics,
            )

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

    def save_metrics(self, metrics: Metrics) -> None:
        """Save current metrics to file.

        Args:
            metrics: Metrics to save
        """
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict
        data = {
            "coverage": {
                "files_total": metrics.coverage.files_total,
                "files_analyzed": metrics.coverage.files_analyzed,
                "files_documented": metrics.coverage.files_documented,
                "coverage_percent": metrics.coverage.coverage_percent,
            },
            "changes": {
                "files_changed": metrics.changes.files_changed,
                "files_changed_percent": metrics.changes.files_changed_percent,
                "files_added": metrics.changes.files_added,
                "files_deleted": metrics.changes.files_deleted,
                "new_languages": metrics.changes.new_languages,
            },
            "quality": {
                "error_count": metrics.quality.error_count,
                "error_rate_percent": metrics.quality.error_rate_percent,
                "warning_count": metrics.quality.warning_count,
                "false_positive_estimate": metrics.quality.false_positive_estimate,
            },
            "performance": {
                "avg_runtime_seconds": metrics.performance.avg_runtime_seconds,
                "memory_usage_mb": metrics.performance.memory_usage_mb,
            },
            "staleness": {
                "last_run_date": metrics.staleness.last_run_date,
                "days_since_last_run": metrics.staleness.days_since_last_run,
            },
            "patterns": {"detected": metrics.patterns.detected, "newly_detected": metrics.patterns.newly_detected},
            "tests": {
                "regression_pass_count": metrics.tests.regression_pass_count,
                "regression_fail_count": metrics.tests.regression_fail_count,
            },
            "user_feedback": {
                "human_override_flags": metrics.user_feedback.human_override_flags,
                "notes": metrics.user_feedback.notes,
            },
        }

        with open(self.metrics_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def calculate_checksum(self, directories: List[str]) -> str:
        """Calculate checksum of critical directories.

        Args:
            directories: List of directory paths relative to codebase root

        Returns:
            SHA256 checksum of directory structure and file names
        """
        hasher = hashlib.sha256()

        for dir_path in directories:
            full_path = self.codebase_path / dir_path
            if not full_path.exists():
                continue

            # Walk directory and hash file paths
            for file_path in sorted(full_path.rglob("*")):
                if file_path.is_file():
                    relative = file_path.relative_to(self.codebase_path)
                    hasher.update(str(relative).encode("utf-8"))

        return hasher.hexdigest()

    def detect_obsolescence(self, current_metrics: Metrics) -> ObsolescenceResult:
        """Detect if tools are obsolete based on metrics.

        Args:
            current_metrics: Current run metrics

        Returns:
            ObsolescenceResult with detection details
        """
        self.current_metrics = current_metrics
        self.previous_metrics = self.load_previous_metrics()

        reasons = []
        is_obsolete = False

        # Check if this is first run
        if self.previous_metrics is None:
            return ObsolescenceResult(
                is_obsolete=False,
                reasons=["First run - no previous metrics"],
                metrics=current_metrics,
                should_regenerate=False,
            )

        # Heuristic 1: Files changed percentage
        if current_metrics.changes.files_changed_percent >= self.thresholds.files_changed_percent:
            is_obsolete = True
            reasons.append(
                f"Files changed: {current_metrics.changes.files_changed_percent:.1f}% "
                f"(threshold: {self.thresholds.files_changed_percent}%)"
            )

        # Heuristic 2: New languages detected
        if self.thresholds.new_languages_detected and current_metrics.changes.new_languages:
            is_obsolete = True
            reasons.append(f"New languages detected: {', '.join(current_metrics.changes.new_languages)}")

        # Heuristic 3: Coverage drop
        if current_metrics.coverage.coverage_percent < self.thresholds.coverage_min_percent:
            is_obsolete = True
            reasons.append(
                f"Coverage dropped: {current_metrics.coverage.coverage_percent:.1f}% "
                f"(minimum: {self.thresholds.coverage_min_percent}%)"
            )

        # Heuristic 4: Staleness
        if current_metrics.staleness.days_since_last_run > self.thresholds.stale_run_days_max:
            is_obsolete = True
            reasons.append(
                f"Stale run: {current_metrics.staleness.days_since_last_run} days "
                f"(max: {self.thresholds.stale_run_days_max})"
            )

        # Heuristic 5: Error rate spike
        if current_metrics.quality.error_rate_percent > self.thresholds.error_rate_max_percent:
            is_obsolete = True
            reasons.append(
                f"High error rate: {current_metrics.quality.error_rate_percent:.1f}% "
                f"(max: {self.thresholds.error_rate_max_percent}%)"
            )

        # Heuristic 6: False positive spike
        if self.previous_metrics:
            prev_fp = self.previous_metrics.quality.false_positive_estimate
            curr_fp = current_metrics.quality.false_positive_estimate
            if prev_fp > 0 and curr_fp > prev_fp * 1.5:  # 50% increase
                is_obsolete = True
                reasons.append(f"False positive spike: {prev_fp} → {curr_fp}")

        # Fallback strategy: Check cooldown period
        should_regenerate = is_obsolete
        suppressed = False
        suppression_reason = ""

        if is_obsolete:
            # Check if we're in cooldown period
            if self.previous_metrics and self.previous_metrics.staleness.last_run_date:
                try:
                    last_run = datetime.fromisoformat(self.previous_metrics.staleness.last_run_date)
                    cooldown_end = last_run + timedelta(days=self.thresholds.regeneration_cooldown_days)

                    if datetime.now() < cooldown_end:
                        should_regenerate = False
                        suppressed = True
                        suppression_reason = f"In cooldown period (ends {cooldown_end.isoformat()})"
                except (ValueError, TypeError):
                    pass

        return ObsolescenceResult(
            is_obsolete=is_obsolete,
            reasons=reasons,
            metrics=current_metrics,
            should_regenerate=should_regenerate,
            suppressed=suppressed,
            suppression_reason=suppression_reason,
        )
