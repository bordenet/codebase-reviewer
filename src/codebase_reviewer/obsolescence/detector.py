"""Obsolescence detection logic for Phase 2 tools."""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from codebase_reviewer.config.loader import ConfigLoader, Phase2ThresholdsConfig
from codebase_reviewer.models_v2 import Metrics


@dataclass
class ObsolescenceThresholds:
    """Thresholds for obsolescence detection.

    These defaults are overridden by config/phase2_thresholds.yml when available.
    """

    files_changed_percent: float = 30.0
    new_languages_detected: bool = True
    coverage_min_percent: float = 85.0
    stale_run_days_max: int = 30
    error_rate_max_percent: float = 5.0
    false_positive_spike_multiplier: float = 1.5
    regeneration_cooldown_days: int = 7

    @classmethod
    def from_config(cls, config: Phase2ThresholdsConfig) -> "ObsolescenceThresholds":
        """Create thresholds from configuration.

        Args:
            config: Phase2ThresholdsConfig loaded from YAML

        Returns:
            ObsolescenceThresholds initialized from config
        """
        return cls(
            files_changed_percent=config.files_changed_percent,
            new_languages_detected=config.new_languages_enabled,
            coverage_min_percent=config.coverage_min_percent,
            stale_run_days_max=config.staleness_max_days,
            error_rate_max_percent=config.error_rate_max_percent,
            false_positive_spike_multiplier=config.false_positive_spike_multiplier,
            regeneration_cooldown_days=config.fallback.cooldown_days,
        )

    @classmethod
    def load_from_config(cls) -> "ObsolescenceThresholds":
        """Load thresholds from configuration file.

        Returns:
            ObsolescenceThresholds initialized from config file
        """
        loader = ConfigLoader()
        config = loader.load_thresholds()
        return cls.from_config(config)


@dataclass
class ObsolescenceTrigger:
    """Details about what triggered obsolescence detection."""

    trigger_type: str  # e.g., "files_changed", "new_languages", "coverage_drop", etc.
    description: str
    current_value: Any
    threshold_value: Any
    recommendation: str = ""


@dataclass
class ObsolescenceResult:
    """Result of obsolescence detection."""

    is_obsolete: bool
    reasons: List[str] = field(default_factory=list)
    triggers: List[ObsolescenceTrigger] = field(default_factory=list)
    metrics: Optional[Metrics] = None
    should_regenerate: bool = False
    suppressed: bool = False
    suppression_reason: str = ""
    threshold_config_yaml: str = ""  # YAML representation of thresholds for prompt embedding

    def get_trigger_types(self) -> List[str]:
        """Get list of trigger type names."""
        return [t.trigger_type for t in self.triggers]

    def get_recommendations(self) -> List[str]:
        """Get list of recommendations from all triggers."""
        return [t.recommendation for t in self.triggers if t.recommendation]


class ObsolescenceDetector:
    """Detects when Phase 2 tools have become obsolete."""

    def __init__(
        self,
        codebase_path: Path,
        metrics_file: Optional[Path] = None,
        thresholds: Optional[ObsolescenceThresholds] = None,
        load_from_config: bool = True,
    ):
        """Initialize detector.

        Args:
            codebase_path: Path to the codebase being analyzed
            metrics_file: Path to metrics JSON file (default: /tmp/codebase-reviewer/{name}/metrics.json)
            thresholds: Custom thresholds (default: load from config file)
            load_from_config: If True and thresholds is None, load from config file
        """
        self.codebase_path = Path(codebase_path)

        # Load thresholds from config if not provided
        if thresholds is not None:
            self.thresholds = thresholds
        elif load_from_config:
            self.thresholds = ObsolescenceThresholds.load_from_config()
        else:
            self.thresholds = ObsolescenceThresholds()

        # Store config loader for threshold YAML generation
        self._config_loader = ConfigLoader()

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

    def _get_recommendation(self, trigger_type: str, **kwargs: Any) -> str:
        """Get recommendation for a trigger type from config.

        Args:
            trigger_type: Type of trigger (e.g., "files_changed")
            **kwargs: Template variables for recommendation

        Returns:
            Recommendation string
        """
        config = self._config_loader.load_thresholds()
        template = config.get_recommendation(trigger_type)
        if template and kwargs:
            # Simple template substitution
            for key, value in kwargs.items():
                template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def detect_obsolescence(self, current_metrics: Metrics) -> ObsolescenceResult:
        """Detect if tools are obsolete based on metrics.

        Args:
            current_metrics: Current run metrics

        Returns:
            ObsolescenceResult with detection details including triggers
        """
        self.current_metrics = current_metrics
        self.previous_metrics = self.load_previous_metrics()

        reasons: List[str] = []
        triggers: List[ObsolescenceTrigger] = []
        is_obsolete = False

        # Check if this is first run
        if self.previous_metrics is None:
            return ObsolescenceResult(
                is_obsolete=False,
                reasons=["First run - no previous metrics"],
                triggers=[],
                metrics=current_metrics,
                should_regenerate=False,
                threshold_config_yaml=self._config_loader.get_threshold_as_yaml(),
            )

        # Heuristic 1: Files changed percentage
        if current_metrics.changes.files_changed_percent >= self.thresholds.files_changed_percent:
            is_obsolete = True
            reason = (
                f"Files changed: {current_metrics.changes.files_changed_percent:.1f}% "
                f"(threshold: {self.thresholds.files_changed_percent}%)"
            )
            reasons.append(reason)
            triggers.append(
                ObsolescenceTrigger(
                    trigger_type="files_changed",
                    description=reason,
                    current_value=current_metrics.changes.files_changed_percent,
                    threshold_value=self.thresholds.files_changed_percent,
                    recommendation=self._get_recommendation("files_changed"),
                )
            )

        # Heuristic 2: New languages detected
        if self.thresholds.new_languages_detected and current_metrics.changes.new_languages:
            is_obsolete = True
            languages = ", ".join(current_metrics.changes.new_languages)
            reason = f"New languages detected: {languages}"
            reasons.append(reason)
            triggers.append(
                ObsolescenceTrigger(
                    trigger_type="new_languages",
                    description=reason,
                    current_value=current_metrics.changes.new_languages,
                    threshold_value="any new language",
                    recommendation=self._get_recommendation("new_languages", languages=languages),
                )
            )

        # Heuristic 3: Coverage drop
        if current_metrics.coverage.coverage_percent < self.thresholds.coverage_min_percent:
            is_obsolete = True
            reason = (
                f"Coverage dropped: {current_metrics.coverage.coverage_percent:.1f}% "
                f"(minimum: {self.thresholds.coverage_min_percent}%)"
            )
            reasons.append(reason)
            triggers.append(
                ObsolescenceTrigger(
                    trigger_type="coverage_drop",
                    description=reason,
                    current_value=current_metrics.coverage.coverage_percent,
                    threshold_value=self.thresholds.coverage_min_percent,
                    recommendation=self._get_recommendation("coverage_drop"),
                )
            )

        # Heuristic 4: Staleness
        if current_metrics.staleness.days_since_last_run > self.thresholds.stale_run_days_max:
            is_obsolete = True
            reason = (
                f"Stale run: {current_metrics.staleness.days_since_last_run} days "
                f"(max: {self.thresholds.stale_run_days_max})"
            )
            reasons.append(reason)
            triggers.append(
                ObsolescenceTrigger(
                    trigger_type="staleness",
                    description=reason,
                    current_value=current_metrics.staleness.days_since_last_run,
                    threshold_value=self.thresholds.stale_run_days_max,
                    recommendation=self._get_recommendation("staleness"),
                )
            )

        # Heuristic 5: Error rate spike
        if current_metrics.quality.error_rate_percent > self.thresholds.error_rate_max_percent:
            is_obsolete = True
            reason = (
                f"High error rate: {current_metrics.quality.error_rate_percent:.1f}% "
                f"(max: {self.thresholds.error_rate_max_percent}%)"
            )
            reasons.append(reason)
            triggers.append(
                ObsolescenceTrigger(
                    trigger_type="error_spike",
                    description=reason,
                    current_value=current_metrics.quality.error_rate_percent,
                    threshold_value=self.thresholds.error_rate_max_percent,
                    recommendation=self._get_recommendation("error_spike"),
                )
            )

        # Heuristic 6: False positive spike
        if self.previous_metrics:
            prev_fp = self.previous_metrics.quality.false_positive_estimate
            curr_fp = current_metrics.quality.false_positive_estimate
            spike_threshold = prev_fp * self.thresholds.false_positive_spike_multiplier
            if prev_fp > 0 and curr_fp > spike_threshold:
                is_obsolete = True
                reason = f"False positive spike: {prev_fp} → {curr_fp}"
                reasons.append(reason)
                triggers.append(
                    ObsolescenceTrigger(
                        trigger_type="false_positive_spike",
                        description=reason,
                        current_value=curr_fp,
                        threshold_value=spike_threshold,
                        recommendation=self._get_recommendation("false_positive_spike"),
                    )
                )

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
            triggers=triggers,
            metrics=current_metrics,
            should_regenerate=should_regenerate,
            suppressed=suppressed,
            suppression_reason=suppression_reason,
            threshold_config_yaml=self._config_loader.get_threshold_as_yaml(),
        )
