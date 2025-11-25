"""Validation framework for comparing LLM outputs vs tool outputs."""

from .comparator import ComparisonResult, DocumentationComparator
from .metrics import FidelityMetrics, calculate_fidelity_score
from .validator import ValidationReport, Validator

__all__ = [
    "DocumentationComparator",
    "ComparisonResult",
    "FidelityMetrics",
    "calculate_fidelity_score",
    "Validator",
    "ValidationReport",
]
