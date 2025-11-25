"""Main validator for end-to-end validation."""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .comparator import ComparisonResult, DocumentationComparator
from .metrics import FidelityMetrics, calculate_metrics_from_comparison


@dataclass
class ValidationReport:
    """Complete validation report."""

    codebase_name: str
    generation: int
    validated_at: datetime

    # Comparison results
    comparison: ComparisonResult
    metrics: FidelityMetrics

    # Overall assessment
    passes_validation: bool
    recommendation: str

    # Detailed findings
    strengths: List[str]
    weaknesses: List[str]
    improvements_needed: List[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "codebase_name": self.codebase_name,
            "generation": self.generation,
            "validated_at": self.validated_at.isoformat(),
            "comparison": {
                "llm_doc_path": self.comparison.llm_doc_path,
                "tool_doc_path": self.comparison.tool_doc_path,
                "similarity_score": self.comparison.similarity_score,
                "sections_compared": self.comparison.sections_compared,
                "sections_matched": self.comparison.sections_matched,
                "quality_assessment": self.comparison.quality_assessment,
            },
            "metrics": self.metrics.to_dict(),
            "passes_validation": self.passes_validation,
            "recommendation": self.recommendation,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "improvements_needed": self.improvements_needed,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def to_markdown(self) -> str:
        """Convert to markdown report."""
        lines = [
            f"# Validation Report: {self.codebase_name} (Gen {self.generation})",
            "",
            f"**Validated**: {self.validated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Overall Assessment",
            "",
            f"**Result**: {'✅ PASS' if self.passes_validation else '❌ FAIL'}",
            f"**Fidelity Score**: {self.metrics.fidelity_score:.1%}",
            f"**Quality Grade**: {self.metrics.quality_grade}",
            "",
            f"**Recommendation**: {self.recommendation}",
            "",
            "## Metrics",
            "",
            f"- **Overall Similarity**: {self.metrics.overall_similarity:.1%}",
            f"- **Content Coverage**: {self.metrics.content_coverage:.1%}",
            f"- **Structure Similarity**: {self.metrics.structure_similarity:.1%}",
            f"- **Completeness**: {self.metrics.completeness:.1%}",
            f"- **Accuracy**: {self.metrics.accuracy:.1%}",
            "",
            "## Section Analysis",
            "",
            f"- **Total Sections**: {self.metrics.sections_total}",
            f"- **Matched Sections**: {self.metrics.sections_matched}",
            f"- **Missing Sections**: {self.metrics.sections_missing}",
            f"- **Extra Sections**: {self.metrics.sections_extra}",
            "",
        ]

        if self.strengths:
            lines.extend(
                [
                    "## Strengths",
                    "",
                    *[f"- {s}" for s in self.strengths],
                    "",
                ]
            )

        if self.weaknesses:
            lines.extend(
                [
                    "## Weaknesses",
                    "",
                    *[f"- {w}" for w in self.weaknesses],
                    "",
                ]
            )

        if self.improvements_needed:
            lines.extend(
                [
                    "## Improvements Needed",
                    "",
                    *[f"- {i}" for i in self.improvements_needed],
                    "",
                ]
            )

        return "\n".join(lines)


class Validator:
    """Validate tool outputs against LLM outputs."""

    def __init__(self, fidelity_threshold: float = 0.95):
        """
        Initialize validator.

        Args:
            fidelity_threshold: Minimum fidelity score to pass (default: 0.95)
        """
        self.fidelity_threshold = fidelity_threshold
        self.comparator = DocumentationComparator()

    def validate(
        self,
        codebase_name: str,
        generation: int,
        llm_doc_path: Path,
        tool_doc_path: Path,
    ) -> ValidationReport:
        """
        Validate tool output against LLM output.

        Args:
            codebase_name: Name of the codebase
            generation: Generation number
            llm_doc_path: Path to LLM-generated documentation
            tool_doc_path: Path to tool-generated documentation

        Returns:
            ValidationReport with complete analysis
        """
        # Compare documents
        comparison = self.comparator.compare(llm_doc_path, tool_doc_path)

        # Calculate metrics
        metrics = calculate_metrics_from_comparison(comparison)

        # Determine if passes validation
        passes = metrics.fidelity_score >= self.fidelity_threshold

        # Generate recommendation
        recommendation = self._generate_recommendation(metrics, passes)

        # Identify strengths and weaknesses
        strengths, weaknesses, improvements = self._analyze_results(comparison, metrics)

        return ValidationReport(
            codebase_name=codebase_name,
            generation=generation,
            validated_at=datetime.now(),
            comparison=comparison,
            metrics=metrics,
            passes_validation=passes,
            recommendation=recommendation,
            strengths=strengths,
            weaknesses=weaknesses,
            improvements_needed=improvements,
        )

    def _generate_recommendation(self, metrics: FidelityMetrics, passes: bool) -> str:
        """Generate recommendation based on metrics."""
        if passes:
            return "Tool output meets quality standards. Ready for production use."
        elif metrics.fidelity_score >= 0.85:
            return "Tool output is good but needs minor improvements to meet 95% threshold."
        elif metrics.fidelity_score >= 0.75:
            return "Tool output needs significant improvements. Consider regenerating with enhanced prompts."
        else:
            return "Tool output quality is insufficient. Regenerate tools with improved meta-prompt."

    def _analyze_results(
        self,
        comparison: ComparisonResult,
        metrics: FidelityMetrics,
    ) -> tuple[List[str], List[str], List[str]]:
        """Analyze results to identify strengths, weaknesses, and improvements."""
        strengths = []
        weaknesses = []
        improvements = []

        # Analyze strengths
        if metrics.overall_similarity >= 0.90:
            strengths.append(f"High overall similarity ({metrics.overall_similarity:.1%})")
        if metrics.content_coverage >= 0.90:
            strengths.append(f"Excellent content coverage ({metrics.content_coverage:.1%})")
        if metrics.completeness >= 0.95:
            strengths.append(f"All expected sections present ({metrics.completeness:.1%})")

        # Analyze weaknesses
        if metrics.overall_similarity < 0.85:
            weaknesses.append(f"Low overall similarity ({metrics.overall_similarity:.1%})")
        if metrics.content_coverage < 0.85:
            weaknesses.append(f"Insufficient content coverage ({metrics.content_coverage:.1%})")
        if metrics.sections_missing > 0:
            weaknesses.append(f"{metrics.sections_missing} sections missing from tool output")

        # Generate improvements
        if metrics.overall_similarity < 0.95:
            improvements.append("Improve text generation to match LLM output more closely")
        if metrics.sections_missing > 0:
            improvements.append(f"Add missing sections: {', '.join(comparison.missing_in_tool[:3])}")
        if metrics.structure_similarity < 0.90:
            improvements.append("Improve section structure to match LLM output")

        return strengths, weaknesses, improvements
