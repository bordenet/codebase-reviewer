"""Improvement engine for prompt optimization.

Analyzes evaluation results and recommends specific prompt improvements.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from codebase_reviewer.tuning.evaluator import EvaluationResult


@dataclass
class ImprovementRecommendation:
    """A specific recommendation for improving a prompt."""

    recommendation_id: str
    priority: str  # HIGH, MEDIUM, LOW
    issue_identified: str
    root_cause: str
    current_prompt_excerpt: str
    improved_prompt_excerpt: str
    expected_impact: Dict[str, str]  # criterion -> expected improvement
    affected_prompts: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = [
            f"## Recommendation #{self.recommendation_id}",
            f"",
            f"**Priority**: {self.priority}",
            f"",
            f"### Issue Identified",
            f"{self.issue_identified}",
            f"",
            f"### Root Cause",
            f"{self.root_cause}",
            f"",
            f"### Proposed Change",
            f"",
            f"**Current Prompt (excerpt)**:",
            f"```",
            f"{self.current_prompt_excerpt}",
            f"```",
            f"",
            f"**Improved Prompt (excerpt)**:",
            f"```",
            f"{self.improved_prompt_excerpt}",
            f"```",
            f"",
            f"### Expected Impact",
        ]

        for criterion, impact in self.expected_impact.items():
            lines.append(f"- **{criterion.title()}**: {impact}")

        lines.extend(["", f"**Affected Prompts**: {', '.join(self.affected_prompts)}", ""])

        return "\n".join(lines)


class ImprovementEngine:
    """Analyzes evaluation results and generates improvement recommendations."""

    def __init__(self):
        """Initialize the improvement engine."""
        self.recommendations: List[ImprovementRecommendation] = []

    def analyze_results(
        self, results: List[EvaluationResult], threshold: float = 3.5
    ) -> List[ImprovementRecommendation]:
        """Analyze evaluation results and generate recommendations.

        Args:
            results: List of evaluation results to analyze
            threshold: Score threshold below which to generate recommendations

        Returns:
            List of improvement recommendations
        """
        if not results:
            return []

        # Group results by prompt
        by_prompt: Dict[str, List[EvaluationResult]] = {}
        for result in results:
            if result.prompt_id not in by_prompt:
                by_prompt[result.prompt_id] = []
            by_prompt[result.prompt_id].append(result)

        # Analyze each prompt
        recommendations = []
        for prompt_id, prompt_results in by_prompt.items():
            # Calculate average scores per criterion
            criterion_scores: Dict[str, List[int]] = {}
            for result in prompt_results:
                for criterion, score in result.scores.items():
                    if criterion not in criterion_scores:
                        criterion_scores[criterion] = []
                    criterion_scores[criterion].append(score)

            # Find low-scoring criteria
            for criterion, scores in criterion_scores.items():
                avg_score = sum(scores) / len(scores)
                if avg_score < threshold:
                    # Generate recommendation
                    rec = self._generate_recommendation(
                        prompt_id=prompt_id,
                        criterion=criterion,
                        avg_score=avg_score,
                        results=prompt_results,
                    )
                    recommendations.append(rec)

        self.recommendations = recommendations
        return recommendations

    def _generate_recommendation(
        self,
        prompt_id: str,
        criterion: str,
        avg_score: float,
        results: List[EvaluationResult],
    ) -> ImprovementRecommendation:
        """Generate a specific recommendation for a low-scoring criterion."""
        # Collect feedback for this criterion
        feedback_items = []
        for result in results:
            if criterion in result.feedback:
                feedback_items.append(result.feedback[criterion])

        # Determine priority based on score
        if avg_score < 2.5:
            priority = "HIGH"
        elif avg_score < 3.0:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        # Generate recommendation based on criterion
        issue, root_cause, current, improved, impact = self._get_criterion_guidance(criterion, avg_score)

        return ImprovementRecommendation(
            recommendation_id=f"{prompt_id}_{criterion}",
            priority=priority,
            issue_identified=issue,
            root_cause=root_cause,
            current_prompt_excerpt=current,
            improved_prompt_excerpt=improved,
            expected_impact={criterion: impact},
            affected_prompts=[prompt_id],
            metadata={
                "avg_score": avg_score,
                "num_tests": len(results),
                "feedback": feedback_items,
            },
        )

    def _get_criterion_guidance(self, criterion: str, avg_score: float) -> tuple[str, str, str, str, str]:
        """Get improvement guidance for a specific criterion."""
        guidance = {
            "clarity": (
                f"Prompt outputs lack clarity (avg score: {avg_score:.2f})",
                "Prompt may be too vague or use ambiguous language",
                "Analyze the codebase and provide insights.",
                "Analyze the codebase structure, identify the main components, "
                "and provide specific insights about architecture patterns, "
                "code organization, and potential improvements.",
                f"{avg_score:.2f} → 4.0+",
            ),
            "completeness": (
                f"Prompt outputs are incomplete (avg score: {avg_score:.2f})",
                "Prompt doesn't specify all required sections or elements",
                "Review the code.",
                "Review the code and provide:\n1. Architecture overview\n2. Code quality assessment\n"
                "3. Security considerations\n4. Performance analysis\n5. Recommendations",
                f"{avg_score:.2f} → 4.0+",
            ),
            "specificity": (
                f"Prompt outputs lack specificity (avg score: {avg_score:.2f})",
                "Prompt allows for generic responses instead of specific findings",
                "Identify issues in the codebase.",
                "Identify specific issues in the codebase, including:\n- Exact file paths and line numbers\n"
                "- Concrete examples of problematic code\n- Specific recommendations with code snippets",
                f"{avg_score:.2f} → 4.0+",
            ),
            "actionability": (
                f"Prompt outputs are not actionable (avg score: {avg_score:.2f})",
                "Prompt doesn't guide toward concrete next steps",
                "Provide recommendations.",
                "Provide actionable recommendations with:\n- Priority level (HIGH/MEDIUM/LOW)\n"
                "- Specific steps to implement\n- Expected impact\n- Estimated effort",
                f"{avg_score:.2f} → 4.0+",
            ),
        }

        return guidance.get(
            criterion,
            (
                f"Low score for {criterion} (avg: {avg_score:.2f})",
                "Prompt may need refinement for this criterion",
                "[Current prompt excerpt]",
                "[Improved prompt excerpt]",
                f"{avg_score:.2f} → 4.0+",
            ),
        )

    def generate_report(self, output_path: Path):
        """Generate a markdown improvement recommendations report."""
        if not self.recommendations:
            raise ValueError("No recommendations to report")

        lines = [
            "# Prompt Improvement Recommendations",
            "",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**Total Recommendations**: {len(self.recommendations)}",
            "",
            "## Summary",
            "",
        ]

        # Count by priority
        priority_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for rec in self.recommendations:
            priority_counts[rec.priority] += 1

        for priority, count in priority_counts.items():
            if count > 0:
                lines.append(f"- **{priority} Priority**: {count} recommendations")

        lines.extend(["", "---", ""])

        # Add each recommendation
        for rec in sorted(
            self.recommendations,
            key=lambda r: (r.priority != "HIGH", r.priority != "MEDIUM"),
        ):
            lines.append(rec.to_markdown())
            lines.append("---\n")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
