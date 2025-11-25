"""Tuning workflow runner - orchestrates the complete prompt tuning process."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from codebase_reviewer.tuning.evaluator import EvaluationResult, PromptEvaluator
from codebase_reviewer.tuning.improvement import ImprovementEngine
from codebase_reviewer.tuning.test_generator import TestDataGenerator


class TuningRunner:
    """Orchestrates the complete prompt tuning workflow."""

    def __init__(self, output_dir: Path):
        """Initialize the tuning runner.

        Args:
            output_dir: Directory to save tuning results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.test_generator = TestDataGenerator()
        self.evaluator = PromptEvaluator()
        self.improvement_engine = ImprovementEngine()

    def run_full_tuning_workflow(
        self,
        project_name: str = "codebase_reviewer",
        num_test_cases: int = 5,
        quality_threshold: float = 3.5,
    ) -> Path:
        """Run the complete tuning workflow.

        Args:
            project_name: Name of the project being tuned
            num_test_cases: Number of test cases to generate
            quality_threshold: Score threshold for generating recommendations

        Returns:
            Path to the tuning results directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = self.output_dir / f"tuning_{project_name}_{timestamp}"
        session_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n🔧 Starting Prompt Tuning Workflow")
        print(f"   Project: {project_name}")
        print(f"   Output: {session_dir}")
        print()

        # Phase 1: Generate test data
        print("📝 Phase 1: Generating test data...")
        test_cases = self.test_generator.generate_codebase_review_tests(num_test_cases)
        test_cases_path = session_dir / "test_cases.json"
        self.test_generator.save_test_cases(test_cases_path, project_name)
        print(f"   ✓ Generated {len(test_cases)} test cases")
        print(f"   ✓ Saved to: {test_cases_path}")
        print()

        # Phase 2: Run simulations (manual step - requires AI agent)
        print("🤖 Phase 2: Run simulations")
        print("   ⚠️  This phase requires manual execution:")
        print(f"   1. Review test cases in: {test_cases_path}")
        print("   2. Run: review-codebase simulate <repo_path> --workflow <workflow>")
        print("   3. For each test case, simulate the prompt execution")
        print("   4. Save simulation results to: simulation_results.json")
        print()

        # Phase 3: Evaluate quality (requires simulation results)
        print("📊 Phase 3: Evaluate quality")
        print("   ⚠️  This phase requires simulation results:")
        print("   1. Load simulation results")
        print("   2. For each output, score against quality rubric")
        print("   3. Generate evaluation report")
        print()

        # Create placeholder for manual evaluation
        self._create_evaluation_template(session_dir)

        # Phase 4: Generate recommendations (requires evaluation results)
        print("💡 Phase 4: Generate improvement recommendations")
        print("   ⚠️  This phase requires evaluation results:")
        print("   1. Load evaluation results")
        print("   2. Analyze low-scoring criteria")
        print("   3. Generate specific improvement recommendations")
        print()

        # Create placeholder for recommendations
        self._create_recommendations_template(session_dir)

        # Summary
        print("✅ Tuning workflow initialized!")
        print()
        print("📁 Next steps:")
        print(f"   1. Review test cases: {test_cases_path}")
        print(
            f"   2. Run simulations and save results to: {session_dir}/simulation_results.json"
        )
        print(
            f"   3. Evaluate outputs and save to: {session_dir}/evaluation_results.json"
        )
        print(f"   4. Run: review-codebase tune evaluate {session_dir}")
        print()

        return session_dir

    def evaluate_simulation_results(self, session_dir: Path) -> Path:
        """Evaluate simulation results and generate recommendations.

        Args:
            session_dir: Directory containing simulation results

        Returns:
            Path to the evaluation report
        """
        session_dir = Path(session_dir)

        # Load evaluation results
        eval_results_path = session_dir / "evaluation_results.json"
        if not eval_results_path.exists():
            raise FileNotFoundError(
                f"Evaluation results not found: {eval_results_path}\n"
                "Please create this file with evaluation scores for each simulation."
            )

        with open(eval_results_path, "r", encoding="utf-8") as f:
            eval_data = json.load(f)

        # Convert to EvaluationResult objects
        results = []
        for item in eval_data.get("results", []):
            result = EvaluationResult(
                test_id=item["test_id"],
                prompt_id=item["prompt_id"],
                scores=item["scores"],
                average_score=item["average_score"],
                feedback=item.get("feedback", {}),
                metadata=item.get("metadata", {}),
            )
            results.append(result)
            self.evaluator.results.append(result)

        # Generate evaluation report
        eval_report_path = session_dir / "evaluation_report.md"
        self.evaluator.generate_report(eval_report_path)
        print(f"✓ Evaluation report: {eval_report_path}")

        # Generate improvement recommendations
        threshold = eval_data.get("quality_threshold", 3.5)
        recommendations = self.improvement_engine.analyze_results(results, threshold)

        if recommendations:
            rec_report_path = session_dir / "improvement_recommendations.md"
            self.improvement_engine.generate_report(rec_report_path)
            print(f"✓ Recommendations: {rec_report_path}")
            print(f"✓ Generated {len(recommendations)} recommendations")
        else:
            print("✓ No recommendations needed - all scores above threshold!")

        return eval_report_path

    def _create_evaluation_template(self, session_dir: Path):
        """Create a template for manual evaluation."""
        template = {
            "project": "codebase_reviewer",
            "quality_threshold": 3.5,
            "rubric": {
                "clarity": "Is the output clear and easy to understand?",
                "completeness": "Does it cover all necessary aspects?",
                "specificity": "Are findings specific and actionable?",
                "actionability": "Can the output be acted upon immediately?",
                "relevance": "Is the content relevant to the codebase?",
            },
            "results": [
                {
                    "test_id": "test_001",
                    "prompt_id": "0.1",
                    "scores": {
                        "clarity": 4,
                        "completeness": 3,
                        "specificity": 4,
                        "actionability": 3,
                        "relevance": 5,
                    },
                    "average_score": 3.8,
                    "feedback": {
                        "completeness": "Missing some architectural details",
                        "actionability": "Recommendations could be more specific",
                    },
                    "metadata": {},
                }
            ],
        }

        template_path = session_dir / "evaluation_results_template.json"
        with open(template_path, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2)

        print(f"   ✓ Created evaluation template: {template_path}")

    def _create_recommendations_template(self, session_dir: Path):
        """Create a template for recommendations."""
        readme = """# Prompt Tuning Session

## Overview
This directory contains the results of a prompt tuning session.

## Files
- `test_cases.json` - Test cases for evaluation
- `evaluation_results_template.json` - Template for manual evaluation
- `evaluation_results.json` - Your evaluation scores (create this)
- `evaluation_report.md` - Generated evaluation report
- `improvement_recommendations.md` - Generated improvement recommendations

## Workflow
1. Review test cases
2. Run simulations for each test case
3. Evaluate outputs and fill in `evaluation_results.json`
4. Run: `review-codebase tune evaluate <this_directory>`
5. Review recommendations and apply improvements
6. Re-run to validate improvements
"""

        readme_path = session_dir / "README.md"
        readme_path.write_text(readme, encoding="utf-8")
