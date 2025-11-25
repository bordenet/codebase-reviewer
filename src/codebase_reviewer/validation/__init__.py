"""Validation framework for comparing LLM outputs vs tool outputs."""

from .comparator import DocumentationComparator, ComparisonResult
from .metrics import FidelityMetrics, calculate_fidelity_score
from .validator import Validator, ValidationReport

__all__ = [
    "DocumentationComparator",
    "ComparisonResult",
    "FidelityMetrics",
    "calculate_fidelity_score",
    "Validator",
    "ValidationReport",
]
