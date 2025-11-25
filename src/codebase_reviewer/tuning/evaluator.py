"""Quality evaluator for prompt outputs.

Evaluates LLM outputs against structured quality rubrics.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class QualityRubric:
    """A quality rubric for evaluating prompt outputs."""

    name: str
    description: str
    criteria: Dict[str, str]  # criterion_name -> description
    scale_min: int = 1
    scale_max: int = 5

    def validate_score(self, score: int) -> bool:
        """Check if a score is within the valid range."""
        return self.scale_min <= score <= self.scale_max


@dataclass
class EvaluationResult:
    """Result of evaluating a prompt output."""

    test_id: str
    prompt_id: str
    scores: Dict[str, int]  # criterion -> score
    average_score: float
    feedback: Dict[str, str]  # criterion -> detailed feedback
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "test_id": self.test_id,
            "prompt_id": self.prompt_id,
            "scores": self.scores,
            "average_score": self.average_score,
            "feedback": self.feedback,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class PromptEvaluator:
    """Evaluates prompt outputs against quality rubrics."""

    # Default rubric for codebase review prompts
    DEFAULT_RUBRIC = QualityRubric(
        name="Codebase Review Quality",
        description="Evaluates quality of codebase review prompts and outputs",
        criteria={
            "clarity": "Is the prompt/output clear and easy to understand?",
            "completeness": "Does it cover all necessary aspects?",
            "specificity": "Are instructions/findings specific and actionable?",
            "actionability": "Can the output be acted upon immediately?",
            "relevance": "Is the content relevant to the codebase being reviewed?",
        },
    )

    def __init__(self, rubric: Optional[QualityRubric] = None):
        """Initialize the evaluator.

        Args:
            rubric: Quality rubric to use (defaults to DEFAULT_RUBRIC)
        """
        self.rubric = rubric or self.DEFAULT_RUBRIC
        self.results: List[EvaluationResult] = []

    def evaluate_output(
        self,
        test_id: str,
        prompt_id: str,
        output: str,
        scores: Dict[str, int],
        feedback: Optional[Dict[str, str]] = None,
    ) -> EvaluationResult:
        """Evaluate a prompt output.

        Args:
            test_id: ID of the test case
            prompt_id: ID of the prompt being evaluated
            output: The LLM output to evaluate
            scores: Scores for each criterion
            feedback: Optional detailed feedback for each criterion

        Returns:
            EvaluationResult with scores and feedback
        """
        # Validate scores
        for criterion, score in scores.items():
            if criterion not in self.rubric.criteria:
                raise ValueError(f"Unknown criterion: {criterion}")
            if not self.rubric.validate_score(score):
                raise ValueError(
                    f"Score {score} for {criterion} outside valid range "
                    f"[{self.rubric.scale_min}, {self.rubric.scale_max}]"
                )

        # Calculate average
        average_score = sum(scores.values()) / len(scores) if scores else 0.0

        result = EvaluationResult(
            test_id=test_id,
            prompt_id=prompt_id,
            scores=scores,
            average_score=average_score,
            feedback=feedback or {},
            metadata={"output_length": len(output), "rubric_name": self.rubric.name},
        )

        self.results.append(result)
        return result

    def generate_report(self, output_path: Path):
        """Generate a markdown evaluation report.

        Args:
            output_path: Path to save the report
        """
        if not self.results:
            raise ValueError("No evaluation results to report")

        # Calculate aggregate statistics
        all_scores: Dict[str, List[float]] = {}
        for result in self.results:
            for criterion, score in result.scores.items():
                if criterion not in all_scores:
                    all_scores[criterion] = []
                all_scores[criterion].append(score)

        avg_by_criterion = {
            criterion: sum(scores) / len(scores)
            for criterion, scores in all_scores.items()
        }
        overall_avg = sum(avg_by_criterion.values()) / len(avg_by_criterion)

        # Generate markdown report
        lines = [
            f"# Prompt Evaluation Report",
            f"",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**Rubric**: {self.rubric.name}",
            f"**Test Cases**: {len(self.results)}",
            f"",
            f"## Overall Results",
            f"",
            f"**Average Score**: {overall_avg:.2f} / {self.rubric.scale_max}",
            f"",
            f"### Scores by Criterion",
            f"",
        ]

        for criterion, avg_score in sorted(avg_by_criterion.items()):
            lines.append(
                f"- **{criterion.title()}**: {avg_score:.2f} / {self.rubric.scale_max}"
            )

        lines.extend(["", "## Detailed Results", ""])

        for result in self.results:
            lines.extend(
                [
                    f"### Test: {result.test_id} | Prompt: {result.prompt_id}",
                    f"",
                    f"**Average**: {result.average_score:.2f}",
                    f"",
                ]
            )

            for criterion, score in result.scores.items():
                feedback = result.feedback.get(criterion, "No feedback provided")
                lines.append(
                    f"- **{criterion.title()}**: {score}/{self.rubric.scale_max} - {feedback}"
                )

            lines.append("")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
