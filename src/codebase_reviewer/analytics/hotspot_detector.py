"""Hotspot detection for identifying problematic files."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class Hotspot:
    """A code hotspot (file likely to have bugs)."""

    file_path: str
    risk_score: float
    complexity_score: float
    churn_score: float
    bug_count: int
    change_frequency: int
    lines_of_code: int
    reason: str

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "file_path": self.file_path,
            "risk_score": self.risk_score,
            "complexity_score": self.complexity_score,
            "churn_score": self.churn_score,
            "bug_count": self.bug_count,
            "change_frequency": self.change_frequency,
            "lines_of_code": self.lines_of_code,
            "reason": self.reason,
        }


class HotspotDetector:
    """Detects code hotspots using churn and complexity analysis."""

    def __init__(self, repo_path: Path):
        """Initialize hotspot detector.

        Args:
            repo_path: Path to git repository
        """
        self.repo_path = repo_path

    def detect_hotspots(self, file_issues: Dict[str, List], file_metrics: Dict[str, dict]) -> List[Hotspot]:
        """Detect code hotspots.

        Args:
            file_issues: Dictionary mapping file paths to lists of issues
            file_metrics: Dictionary mapping file paths to metrics

        Returns:
            List of hotspots sorted by risk score
        """
        hotspots = []

        # Get churn data from git
        churn_data = self._get_churn_data()

        for file_path, issues in file_issues.items():
            # Calculate metrics
            bug_count = len(issues)
            churn = churn_data.get(file_path, 0)
            metrics = file_metrics.get(file_path, {})
            loc = metrics.get("lines_of_code", 0)

            # Calculate scores
            complexity_score = self._calculate_complexity_score(metrics)
            churn_score = min(churn / 10.0, 10.0)  # Normalize to 0-10

            # Risk score = weighted combination
            risk_score = (bug_count * 3.0 + complexity_score * 2.0 + churn_score * 1.5) / 6.5

            # Only include files with significant risk
            if risk_score > 3.0:
                reason = self._generate_reason(bug_count, complexity_score, churn_score)

                hotspots.append(
                    Hotspot(
                        file_path=file_path,
                        risk_score=round(risk_score, 2),
                        complexity_score=round(complexity_score, 2),
                        churn_score=round(churn_score, 2),
                        bug_count=bug_count,
                        change_frequency=churn,
                        lines_of_code=loc,
                        reason=reason,
                    )
                )

        # Sort by risk score descending
        hotspots.sort(key=lambda h: h.risk_score, reverse=True)

        return hotspots

    def _get_churn_data(self) -> Dict[str, int]:
        """Get file churn data from git.

        Returns:
            Dictionary mapping file paths to change counts
        """
        try:
            # Get file change counts from last 90 days
            result = subprocess.run(
                [
                    "git",
                    "log",
                    "--since=90 days ago",
                    "--name-only",
                    "--pretty=format:",
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                return {}

            # Count occurrences
            churn: Dict[str, int] = {}
            for line in result.stdout.split("\n"):
                line = line.strip()
                if line:
                    churn[line] = churn.get(line, 0) + 1

            return churn
        except Exception:
            return {}

    def _calculate_complexity_score(self, metrics: dict) -> float:
        """Calculate complexity score from metrics.

        Args:
            metrics: File metrics

        Returns:
            Complexity score (0-10)
        """
        # Simple heuristic based on lines of code
        loc = metrics.get("lines_of_code", 0)

        if loc < 100:
            return 1.0
        elif loc < 300:
            return 3.0
        elif loc < 500:
            return 5.0
        elif loc < 1000:
            return 7.0
        else:
            return 9.0

    def _generate_reason(self, bug_count: int, complexity: float, churn: float) -> str:
        """Generate human-readable reason for hotspot.

        Args:
            bug_count: Number of bugs
            complexity: Complexity score
            churn: Churn score

        Returns:
            Reason string
        """
        reasons = []

        if bug_count > 5:
            reasons.append(f"high bug count ({bug_count})")
        elif bug_count > 2:
            reasons.append(f"multiple bugs ({bug_count})")

        if complexity > 7:
            reasons.append("high complexity")
        elif complexity > 5:
            reasons.append("moderate complexity")

        if churn > 7:
            reasons.append("frequently changed")
        elif churn > 4:
            reasons.append("moderately changed")

        return ", ".join(reasons) if reasons else "potential risk"
