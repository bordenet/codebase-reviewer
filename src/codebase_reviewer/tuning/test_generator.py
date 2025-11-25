"""Test data generator for prompt tuning.

Generates realistic test cases for evaluating and improving prompts.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class TestCase:
    """A single test case for prompt evaluation."""

    test_id: str
    name: str
    description: str
    inputs: Dict[str, Any]
    expected_qualities: Optional[Dict[str, int]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.test_id,
            "name": self.name,
            "description": self.description,
            "inputs": self.inputs,
            "expected_qualities": self.expected_qualities or {},
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestCase":
        """Create from dictionary."""
        return cls(
            test_id=data["id"],
            name=data["name"],
            description=data["description"],
            inputs=data["inputs"],
            expected_qualities=data.get("expected_qualities"),
            metadata=data.get("metadata", {}),
        )


class TestDataGenerator:
    """Generates test data for prompt evaluation."""

    def __init__(self):
        """Initialize the test data generator."""
        self.test_cases: List[TestCase] = []

    def generate_codebase_review_tests(self, num_cases: int = 5) -> List[TestCase]:
        """Generate test cases for codebase review prompts.

        Args:
            num_cases: Number of test cases to generate

        Returns:
            List of test cases
        """
        test_cases = []

        # Template test cases with varying characteristics
        templates = [
            {
                "name": "Small Python Library",
                "description": "Simple Python library with good documentation",
                "repo_type": "library",
                "languages": ["Python"],
                "size": "small",
                "doc_quality": "high",
            },
            {
                "name": "Medium TypeScript Web App",
                "description": "React-based web application with moderate complexity",
                "repo_type": "web_app",
                "languages": ["TypeScript", "JavaScript"],
                "size": "medium",
                "doc_quality": "medium",
            },
            {
                "name": "Large Polyglot Microservices",
                "description": "Complex microservices architecture with multiple languages",
                "repo_type": "microservices",
                "languages": ["Go", "Python", "TypeScript"],
                "size": "large",
                "doc_quality": "low",
            },
            {
                "name": "Legacy Java Monolith",
                "description": "Large legacy Java application with minimal documentation",
                "repo_type": "monolith",
                "languages": ["Java"],
                "size": "large",
                "doc_quality": "low",
            },
            {
                "name": "Well-Documented Go CLI Tool",
                "description": "Command-line tool with excellent documentation and tests",
                "repo_type": "cli",
                "languages": ["Go"],
                "size": "small",
                "doc_quality": "high",
            },
        ]

        for i, template in enumerate(templates[:num_cases]):
            test_case = TestCase(
                test_id=f"test_{i+1:03d}",
                name=template["name"],
                description=template["description"],
                inputs={
                    "repo_type": template["repo_type"],
                    "languages": template["languages"],
                    "size": template["size"],
                    "doc_quality": template["doc_quality"],
                },
                expected_qualities={
                    "clarity": 4,
                    "completeness": 4,
                    "actionability": 4,
                    "specificity": 4,
                },
                metadata={"template_index": i},
            )
            test_cases.append(test_case)

        self.test_cases = test_cases
        return test_cases

    def save_test_cases(self, output_path: Path, project_name: str = "codebase_reviewer"):
        """Save test cases to JSON file.

        Args:
            output_path: Path to save the test cases
            project_name: Name of the project being tested
        """
        data = {
            "project": project_name,
            "version": "1.0",
            "test_cases": [tc.to_dict() for tc in self.test_cases],
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_test_cases(self, input_path: Path) -> List[TestCase]:
        """Load test cases from JSON file.

        Args:
            input_path: Path to the test cases file

        Returns:
            List of test cases
        """
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.test_cases = [TestCase.from_dict(tc) for tc in data["test_cases"]]
        return self.test_cases
