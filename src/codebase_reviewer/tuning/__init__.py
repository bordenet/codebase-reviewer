"""Prompt tuning system for systematic LLM prompt improvement.

This package provides tools for:
1. Generating test data for prompt evaluation
2. Running simulations with test data
3. Evaluating prompt quality against rubrics
4. Recommending specific improvements

Based on the generalized prompt tuning methodology from the archive.
"""

from codebase_reviewer.tuning.evaluator import (
    PromptEvaluator,
    QualityRubric,
    EvaluationResult,
)
from codebase_reviewer.tuning.improvement import (
    ImprovementEngine,
    ImprovementRecommendation,
)
from codebase_reviewer.tuning.test_generator import TestDataGenerator, TestCase

__all__ = [
    "TestDataGenerator",
    "TestCase",
    "PromptEvaluator",
    "QualityRubric",
    "EvaluationResult",
    "ImprovementEngine",
    "ImprovementRecommendation",
]
