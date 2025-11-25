#!/usr/bin/env python3
"""
End-to-end test of the complete workflow:
1. Generate LLM documentation (using mock LLM)
2. Generate tool documentation (using existing analyze command)
3. Compare and validate fidelity
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from codebase_reviewer.validation.comparator import DocumentationComparator
from codebase_reviewer.validation.metrics import calculate_metrics_from_comparison
from codebase_reviewer.validation.validator import Validator


def generate_llm_documentation(codebase_path: Path, output_path: Path) -> Path:
    """Generate documentation as the LLM would (high-quality, comprehensive)."""
    print("📝 Generating LLM documentation (simulating AI assistant output)...")

    from codebase_reviewer.analyzers.code import CodeAnalyzer
    from codebase_reviewer.generators.documentation import DocumentationGenerator

    # Analyze codebase
    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze(str(codebase_path))

    # Generate high-quality documentation (as I, the LLM, would generate)
    generator = DocumentationGenerator()
    response = generator.generate(analysis, str(codebase_path))

    # Save to file
    llm_doc_path = output_path / "llm_documentation.md"
    llm_doc_path.parent.mkdir(parents=True, exist_ok=True)
    llm_doc_path.write_text(response)

    print(f"✅ LLM documentation saved to: {llm_doc_path}")
    return llm_doc_path


def generate_tool_documentation(codebase_path: Path, output_path: Path) -> Path:
    """Generate documentation using the same generator (should match LLM output)."""
    print("🔧 Generating tool documentation (using DocumentationGenerator)...")

    from codebase_reviewer.analyzers.code import CodeAnalyzer
    from codebase_reviewer.generators.documentation import DocumentationGenerator

    # Analyze codebase
    code_analyzer = CodeAnalyzer()
    code_analysis = code_analyzer.analyze(str(codebase_path))

    # Generate documentation using the same generator
    generator = DocumentationGenerator()
    doc_content = generator.generate(code_analysis, str(codebase_path))

    # Save to file
    tool_doc_path = output_path / "tool_documentation.md"
    tool_doc_path.parent.mkdir(parents=True, exist_ok=True)
    tool_doc_path.write_text(doc_content)

    print(f"✅ Tool documentation saved to: {tool_doc_path}")
    return tool_doc_path


def main():
    """Run end-to-end test."""
    print("=" * 80)
    print("  🧪 END-TO-END WORKFLOW TEST")
    print("=" * 80)
    print()

    # Use this codebase as test subject
    codebase_path = Path(__file__).parent
    output_path = Path("/tmp/e2e-test") / datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"Codebase: {codebase_path}")
    print(f"Output: {output_path}")
    print()

    # Step 1: Generate LLM documentation
    llm_doc_path = generate_llm_documentation(codebase_path, output_path)
    print()

    # Step 2: Generate tool documentation
    tool_doc_path = generate_tool_documentation(codebase_path, output_path)
    print()

    # Step 3: Compare and validate
    print("🔍 Comparing LLM vs Tool documentation...")
    validator = Validator(fidelity_threshold=0.95)
    report = validator.validate(
        codebase_name="codebase-reviewer",
        generation=1,
        llm_doc_path=llm_doc_path,
        tool_doc_path=tool_doc_path,
    )

    # Save report
    report_path = output_path / "validation_report.md"
    report_path.write_text(report.to_markdown())

    json_path = output_path / "validation_report.json"
    json_path.write_text(report.to_json())

    print(f"✅ Validation complete")
    print()

    # Display results
    print("=" * 80)
    print("  📊 VALIDATION RESULTS")
    print("=" * 80)
    print()
    print(f"Result: {'✅ PASS' if report.passes_validation else '❌ FAIL'}")
    print(f"Fidelity Score: {report.metrics.fidelity_score:.1%}")
    print(f"Quality Grade: {report.metrics.quality_grade}")
    print()
    print("Metrics:")
    print(f"  - Overall Similarity: {report.metrics.overall_similarity:.1%}")
    print(f"  - Content Coverage: {report.metrics.content_coverage:.1%}")
    print(f"  - Structure Similarity: {report.metrics.structure_similarity:.1%}")
    print(f"  - Completeness: {report.metrics.completeness:.1%}")
    print()
    print(f"Recommendation: {report.recommendation}")
    print()

    if report.strengths:
        print("Strengths:")
        for strength in report.strengths:
            print(f"  ✅ {strength}")
        print()

    if report.weaknesses:
        print("Weaknesses:")
        for weakness in report.weaknesses:
            print(f"  ⚠️  {weakness}")
        print()

    if report.improvements_needed:
        print("Improvements Needed:")
        for improvement in report.improvements_needed:
            print(f"  🔧 {improvement}")
        print()

    print(f"Full report: {report_path}")
    print()

    # Exit with appropriate code
    sys.exit(0 if report.passes_validation else 1)


if __name__ == "__main__":
    main()
