"""Fidelity metrics for validation."""

from dataclasses import dataclass
from typing import Dict, List
import json


@dataclass
class FidelityMetrics:
    """Metrics for measuring fidelity between LLM and tool outputs."""

    overall_similarity: float  # 0.0 to 1.0
    content_coverage: float  # 0.0 to 1.0 (how much of LLM content is in tool output)
    structure_similarity: float  # 0.0 to 1.0 (section structure match)
    completeness: float  # 0.0 to 1.0 (all expected sections present)
    accuracy: float  # 0.0 to 1.0 (factual correctness)
    fidelity_score: float  # 0.0 to 1.0 (weighted average)

    # Detailed metrics
    sections_total: int
    sections_matched: int
    sections_missing: int
    sections_extra: int

    # Quality assessment
    quality_grade: str  # "A", "B", "C", "D", "F"
    passes_threshold: bool  # True if >= 95%

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "overall_similarity": self.overall_similarity,
            "content_coverage": self.content_coverage,
            "structure_similarity": self.structure_similarity,
            "completeness": self.completeness,
            "accuracy": self.accuracy,
            "fidelity_score": self.fidelity_score,
            "sections_total": self.sections_total,
            "sections_matched": self.sections_matched,
            "sections_missing": self.sections_missing,
            "sections_extra": self.sections_extra,
            "quality_grade": self.quality_grade,
            "passes_threshold": self.passes_threshold,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


def calculate_fidelity_score(
    overall_similarity: float,
    content_coverage: float,
    structure_similarity: float,
    completeness: float,
    accuracy: float = 1.0,
) -> float:
    """
    Calculate weighted fidelity score.

    Weights:
    - Overall similarity: 30%
    - Content coverage: 25%
    - Structure similarity: 20%
    - Completeness: 15%
    - Accuracy: 10%

    Args:
        overall_similarity: Overall text similarity (0.0 to 1.0)
        content_coverage: How much LLM content is covered (0.0 to 1.0)
        structure_similarity: Section structure match (0.0 to 1.0)
        completeness: All expected sections present (0.0 to 1.0)
        accuracy: Factual correctness (0.0 to 1.0, default: 1.0)

    Returns:
        Weighted fidelity score (0.0 to 1.0)
    """
    weights = {
        "overall_similarity": 0.30,
        "content_coverage": 0.25,
        "structure_similarity": 0.20,
        "completeness": 0.15,
        "accuracy": 0.10,
    }

    score = (
        overall_similarity * weights["overall_similarity"]
        + content_coverage * weights["content_coverage"]
        + structure_similarity * weights["structure_similarity"]
        + completeness * weights["completeness"]
        + accuracy * weights["accuracy"]
    )

    return score


def calculate_metrics_from_comparison(comparison_result) -> FidelityMetrics:
    """
    Calculate fidelity metrics from comparison result.

    Args:
        comparison_result: ComparisonResult from DocumentationComparator

    Returns:
        FidelityMetrics with all calculated metrics
    """
    # Calculate individual metrics
    overall_similarity = comparison_result.similarity_score

    # Content coverage: how many sections from LLM are in tool output
    if comparison_result.sections_compared > 0:
        content_coverage = (
            comparison_result.sections_matched / comparison_result.sections_compared
        )
    else:
        content_coverage = 1.0

    # Structure similarity: section structure match
    total_sections = (
        comparison_result.sections_compared
        + len(comparison_result.missing_in_tool)
        + len(comparison_result.missing_in_llm)
    )
    if total_sections > 0:
        structure_similarity = comparison_result.sections_compared / total_sections
    else:
        structure_similarity = 1.0

    # Completeness: all expected sections present
    if comparison_result.sections_compared > 0:
        completeness = 1.0 - (
            len(comparison_result.missing_in_tool) / comparison_result.sections_compared
        )
    else:
        completeness = 1.0

    # Accuracy: assume 100% for now (would need manual review)
    accuracy = 1.0

    # Calculate fidelity score
    fidelity_score = calculate_fidelity_score(
        overall_similarity,
        content_coverage,
        structure_similarity,
        completeness,
        accuracy,
    )

    # Determine quality grade
    if fidelity_score >= 0.95:
        quality_grade = "A"
    elif fidelity_score >= 0.85:
        quality_grade = "B"
    elif fidelity_score >= 0.75:
        quality_grade = "C"
    elif fidelity_score >= 0.65:
        quality_grade = "D"
    else:
        quality_grade = "F"

    # Check if passes threshold (95%)
    passes_threshold = fidelity_score >= 0.95

    return FidelityMetrics(
        overall_similarity=overall_similarity,
        content_coverage=content_coverage,
        structure_similarity=structure_similarity,
        completeness=completeness,
        accuracy=accuracy,
        fidelity_score=fidelity_score,
        sections_total=total_sections,
        sections_matched=comparison_result.sections_matched,
        sections_missing=len(comparison_result.missing_in_tool),
        sections_extra=len(comparison_result.missing_in_llm),
        quality_grade=quality_grade,
        passes_threshold=passes_threshold,
    )
