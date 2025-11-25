"""Risk scoring for prioritizing issues."""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class ImpactLevel(Enum):
    """Business impact level."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class RiskScore:
    """Risk score for an issue."""

    issue_id: str
    file_path: str
    severity: str
    impact: str
    effort_minutes: int
    risk_score: float
    priority: str  # 'critical', 'high', 'medium', 'low'
    is_quick_win: bool
    recommendation: str

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "issue_id": self.issue_id,
            "file_path": self.file_path,
            "severity": self.severity,
            "impact": self.impact,
            "effort_minutes": self.effort_minutes,
            "risk_score": self.risk_score,
            "priority": self.priority,
            "is_quick_win": self.is_quick_win,
            "recommendation": self.recommendation,
        }


class RiskScorer:
    """Scores and prioritizes issues based on risk and impact."""

    def __init__(self):
        """Initialize risk scorer."""
        self.severity_weights = {
            "critical": 10.0,
            "high": 7.0,
            "medium": 4.0,
            "low": 2.0,
            "info": 1.0,
        }

        self.impact_weights = {
            "critical": 10.0,
            "high": 7.0,
            "medium": 4.0,
            "low": 2.0,
        }

    def score_issues(
        self, issues: List[dict], hotspots: List[dict] = None
    ) -> List[RiskScore]:
        """Score and prioritize issues.

        Args:
            issues: List of issues to score
            hotspots: Optional list of hotspots for context

        Returns:
            List of risk scores sorted by priority
        """
        hotspot_files = set()
        if hotspots:
            hotspot_files = {h.get("file_path") for h in hotspots}

        risk_scores = []

        for issue in issues:
            # Extract issue details
            severity = issue.get("severity", "low").lower()
            file_path = issue.get("file_path", "")
            effort = issue.get("effort_minutes", 30)

            # Determine impact
            impact = self._determine_impact(severity, file_path, hotspot_files)

            # Calculate risk score
            severity_weight = self.severity_weights.get(severity, 1.0)
            impact_weight = self.impact_weights.get(impact, 2.0)

            # Risk = (Severity * Impact) / Effort
            # Higher risk = more important to fix
            risk_score = (severity_weight * impact_weight) / (effort / 30.0)

            # Determine priority
            priority = self._determine_priority(risk_score)

            # Check if quick win (high impact, low effort)
            is_quick_win = impact_weight >= 7.0 and effort <= 30

            # Generate recommendation
            recommendation = self._generate_recommendation(
                severity, impact, effort, is_quick_win, file_path in hotspot_files
            )

            risk_scores.append(
                RiskScore(
                    issue_id=issue.get("id", ""),
                    file_path=file_path,
                    severity=severity,
                    impact=impact,
                    effort_minutes=effort,
                    risk_score=round(risk_score, 2),
                    priority=priority,
                    is_quick_win=is_quick_win,
                    recommendation=recommendation,
                )
            )

        # Sort by risk score descending
        risk_scores.sort(key=lambda r: r.risk_score, reverse=True)

        return risk_scores

    def _determine_impact(
        self, severity: str, file_path: str, hotspot_files: set
    ) -> str:
        """Determine business impact of an issue.

        Args:
            severity: Issue severity
            file_path: File path
            hotspot_files: Set of hotspot file paths

        Returns:
            Impact level
        """
        # Security issues have higher impact
        if severity == "critical":
            return "critical"

        # Issues in hotspots have higher impact
        if file_path in hotspot_files:
            if severity == "high":
                return "critical"
            elif severity == "medium":
                return "high"
            else:
                return "medium"

        # Default mapping
        if severity == "high":
            return "high"
        elif severity == "medium":
            return "medium"
        else:
            return "low"

    def _determine_priority(self, risk_score: float) -> str:
        """Determine priority from risk score.

        Args:
            risk_score: Calculated risk score

        Returns:
            Priority level
        """
        if risk_score >= 20:
            return "critical"
        elif risk_score >= 10:
            return "high"
        elif risk_score >= 5:
            return "medium"
        else:
            return "low"

    def _generate_recommendation(
        self,
        severity: str,
        impact: str,
        effort: int,
        is_quick_win: bool,
        in_hotspot: bool,
    ) -> str:
        """Generate recommendation for issue.

        Args:
            severity: Issue severity
            impact: Business impact
            effort: Effort in minutes
            is_quick_win: Whether this is a quick win
            in_hotspot: Whether in a hotspot file

        Returns:
            Recommendation string
        """
        if is_quick_win:
            return "Quick win - fix immediately for high impact with low effort"

        if severity == "critical":
            return "Critical security issue - fix immediately"

        if in_hotspot and impact in ["critical", "high"]:
            return "High-risk file with significant issues - prioritize for refactoring"

        if impact == "critical":
            return "High business impact - schedule for next sprint"

        if effort <= 15:
            return "Low effort fix - good candidate for quick improvement"

        if effort >= 120:
            return "High effort - consider breaking into smaller tasks"

        return "Standard priority - address in normal workflow"
