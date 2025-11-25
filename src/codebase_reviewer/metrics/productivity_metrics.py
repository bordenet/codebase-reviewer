"""Developer productivity metrics and tracking."""

import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ProductivityMetrics:
    """Developer productivity metrics."""

    # Code metrics
    lines_of_code: int = 0
    files_changed: int = 0
    commits_count: int = 0

    # Quality metrics
    bugs_fixed: int = 0
    bugs_introduced: int = 0
    code_review_comments: int = 0

    # Time metrics
    avg_commit_time: float = 0.0  # hours
    avg_pr_time: float = 0.0  # hours
    avg_review_time: float = 0.0  # hours

    # Efficiency metrics
    code_churn: float = 0.0  # % of code rewritten
    test_coverage: float = 0.0  # %
    documentation_coverage: float = 0.0  # %

    # Collaboration metrics
    pr_reviews_given: int = 0
    pr_reviews_received: int = 0
    pair_programming_hours: float = 0.0


@dataclass
class ProductivityReport:
    """Productivity report for a developer or team."""

    period_start: datetime
    period_end: datetime
    metrics: ProductivityMetrics
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    productivity_score: float = 0.0

    def __post_init__(self):
        """Calculate productivity score."""
        self.productivity_score = self._calculate_score()

    def _calculate_score(self) -> float:
        """Calculate overall productivity score (0-100).

        Returns:
            Productivity score
        """
        score = 0.0

        # Code output (20 points)
        if self.metrics.commits_count > 0:
            score += min(20, self.metrics.commits_count * 2)

        # Quality (30 points)
        if self.metrics.bugs_introduced > 0:
            bug_ratio = self.metrics.bugs_fixed / self.metrics.bugs_introduced
            score += min(15, bug_ratio * 15)
        else:
            score += 15

        if self.metrics.test_coverage > 0:
            score += min(15, self.metrics.test_coverage / 100 * 15)

        # Efficiency (25 points)
        if self.metrics.code_churn < 30:  # Low churn is good
            score += 15
        elif self.metrics.code_churn < 50:
            score += 10
        else:
            score += 5

        if self.metrics.avg_commit_time > 0 and self.metrics.avg_commit_time < 4:
            score += 10  # Fast commits are good

        # Collaboration (25 points)
        score += min(15, self.metrics.pr_reviews_given * 3)
        score += min(10, self.metrics.code_review_comments / 10)

        return min(100, score)


class ProductivityTracker:
    """Track developer productivity metrics."""

    def __init__(self, repo_path: Path):
        """Initialize productivity tracker.

        Args:
            repo_path: Path to repository
        """
        self.repo_path = Path(repo_path)

    def generate_report(
        self, days: int = 30, author: Optional[str] = None
    ) -> ProductivityReport:
        """Generate productivity report.

        Args:
            days: Number of days to analyze
            author: Git author to filter by (None for all)

        Returns:
            Productivity report
        """
        period_end = datetime.now()
        period_start = period_end - timedelta(days=days)

        metrics = self._collect_metrics(period_start, period_end, author)
        insights = self._generate_insights(metrics)
        recommendations = self._generate_recommendations(metrics)

        return ProductivityReport(
            period_start=period_start,
            period_end=period_end,
            metrics=metrics,
            insights=insights,
            recommendations=recommendations,
        )

    def _collect_metrics(
        self, start: datetime, end: datetime, author: Optional[str]
    ) -> ProductivityMetrics:
        """Collect productivity metrics from git history.

        Args:
            start: Start date
            end: End date
            author: Git author filter

        Returns:
            Productivity metrics
        """
        metrics = ProductivityMetrics()

        try:
            # Get commit count
            cmd = [
                "git",
                "log",
                "--oneline",
                f"--since={start.isoformat()}",
                f"--until={end.isoformat()}",
            ]
            if author:
                cmd.extend(["--author", author])

            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True
            )
            metrics.commits_count = (
                len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            )

            # Get files changed
            cmd = [
                "git",
                "log",
                "--name-only",
                "--pretty=format:",
                f"--since={start.isoformat()}",
                f"--until={end.isoformat()}",
            ]
            if author:
                cmd.extend(["--author", author])

            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True
            )
            files = set(line for line in result.stdout.strip().split("\n") if line)
            metrics.files_changed = len(files)

            # Get lines of code changed
            cmd = [
                "git",
                "log",
                "--numstat",
                "--pretty=format:",
                f"--since={start.isoformat()}",
                f"--until={end.isoformat()}",
            ]
            if author:
                cmd.extend(["--author", author])

            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True
            )
            total_lines = 0
            for line in result.stdout.strip().split("\n"):
                if line and "\t" in line:
                    parts = line.split("\t")
                    if len(parts) >= 2 and parts[0].isdigit():
                        total_lines += int(parts[0])
            metrics.lines_of_code = total_lines

            # Calculate code churn (simplified)
            if metrics.lines_of_code > 0:
                metrics.code_churn = min(
                    100, (metrics.files_changed / max(1, metrics.commits_count)) * 10
                )

        except Exception:
            pass  # Return empty metrics on error

        return metrics

    def _generate_insights(self, metrics: ProductivityMetrics) -> List[str]:
        """Generate insights from metrics.

        Args:
            metrics: Productivity metrics

        Returns:
            List of insights
        """
        insights = []

        if metrics.commits_count > 20:
            insights.append("High commit frequency indicates active development")
        elif metrics.commits_count < 5:
            insights.append("Low commit frequency - consider more frequent commits")

        if metrics.code_churn > 50:
            insights.append("High code churn detected - code may be unstable")
        elif metrics.code_churn < 20:
            insights.append("Low code churn indicates stable codebase")

        if metrics.files_changed > 50:
            insights.append("Many files changed - consider breaking into smaller PRs")

        return insights

    def _generate_recommendations(self, metrics: ProductivityMetrics) -> List[str]:
        """Generate recommendations from metrics.

        Args:
            metrics: Productivity metrics

        Returns:
            List of recommendations
        """
        recommendations = []

        if metrics.test_coverage < 80:
            recommendations.append("Increase test coverage to improve code quality")

        if metrics.code_churn > 50:
            recommendations.append(
                "Reduce code churn by planning changes more carefully"
            )

        if metrics.pr_reviews_given < 5:
            recommendations.append(
                "Participate more in code reviews to improve collaboration"
            )

        if metrics.documentation_coverage < 50:
            recommendations.append("Add more documentation to improve maintainability")

        return recommendations
