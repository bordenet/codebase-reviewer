# Prompt Tuning Guide

**Systematic LLM Prompt Improvement for Codebase Reviewer**

## Overview

The prompt tuning system provides a structured workflow for improving LLM prompts through:

1. **Test Data Generation** - Create realistic test cases
2. **Simulation** - Execute prompts with test data
3. **Evaluation** - Score outputs against quality rubrics
4. **Improvement** - Generate specific recommendations

This system is based on the generalized prompt tuning methodology documented in the `archive/` directory.

## Quick Start

### 1. Initialize a Tuning Session

```bash
# Create a new tuning session
review-codebase tune init --project codebase_reviewer --num-tests 5

# Output:
# ✅ Tuning session initialized: ./prompt_tuning_results/tuning_codebase_reviewer_YYYYMMDD_HHMMSS
```

This creates:
- `test_cases.json` - Generated test cases
- `evaluation_results_template.json` - Template for manual evaluation
- `README.md` - Session instructions

### 2. Run Simulations

For each test case, run the simulation:

```bash
# Run simulation on a repository
review-codebase simulate /path/to/repo --workflow reviewer_criteria

# Review the generated prompts in simulation_results/
```

### 3. Evaluate Outputs

Manually evaluate each simulation output:

1. Copy `evaluation_results_template.json` to `evaluation_results.json`
2. For each test case, score the output against the rubric:
   - **Clarity** (1-5): Is the output clear and understandable?
   - **Completeness** (1-5): Does it cover all necessary aspects?
   - **Specificity** (1-5): Are findings specific and actionable?
   - **Actionability** (1-5): Can it be acted upon immediately?
   - **Relevance** (1-5): Is it relevant to the codebase?

3. Add detailed feedback for low scores

Example `evaluation_results.json`:

```json
{
  "project": "codebase_reviewer",
  "quality_threshold": 3.5,
  "rubric": {
    "clarity": "Is the output clear and easy to understand?",
    "completeness": "Does it cover all necessary aspects?",
    "specificity": "Are findings specific and actionable?",
    "actionability": "Can the output be acted upon immediately?",
    "relevance": "Is the content relevant to the codebase?"
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
        "relevance": 5
      },
      "average_score": 3.8,
      "feedback": {
        "completeness": "Missing architectural details about component interactions",
        "actionability": "Recommendations need specific file paths and code examples"
      }
    }
  ]
}
```

### 4. Generate Recommendations

```bash
# Analyze evaluation results and generate recommendations
review-codebase tune evaluate ./prompt_tuning_results/tuning_codebase_reviewer_YYYYMMDD_HHMMSS

# Output:
# ✓ Evaluation report: evaluation_report.md
# ✓ Recommendations: improvement_recommendations.md
# ✓ Generated 3 recommendations
```

### 5. Apply Improvements

Review the recommendations in `improvement_recommendations.md`:

- Each recommendation includes:
  - Priority (HIGH/MEDIUM/LOW)
  - Issue identified
  - Root cause
  - Current vs. improved prompt excerpt
  - Expected impact

Apply the improvements to your prompt templates in:
- `src/codebase_reviewer/prompts/workflows/`
- `src/codebase_reviewer/prompts/templates/`

### 6. Validate Improvements

Re-run the tuning workflow with the improved prompts:

```bash
# Initialize new session
review-codebase tune init --project codebase_reviewer_v2

# Run simulations with improved prompts
# Evaluate and compare scores
```

## Quality Rubric

### Default Rubric for Codebase Review

| Criterion | Description | Target Score |
|-----------|-------------|--------------|
| **Clarity** | Output is clear, well-structured, and easy to understand | 4.0+ |
| **Completeness** | All required sections and elements are present | 4.0+ |
| **Specificity** | Findings include specific file paths, line numbers, examples | 4.0+ |
| **Actionability** | Recommendations are concrete with clear next steps | 4.0+ |
| **Relevance** | Content is directly relevant to the codebase analyzed | 4.0+ |

### Scoring Scale

- **5** - Excellent: Exceeds expectations
- **4** - Good: Meets expectations
- **3** - Acceptable: Minor improvements needed
- **2** - Poor: Significant improvements needed
- **1** - Unacceptable: Major issues

## Advanced Usage

### Custom Test Cases

Create custom test cases by editing `test_cases.json`:

```json
{
  "id": "test_custom",
  "name": "Custom Test Case",
  "description": "Description of the test scenario",
  "inputs": {
    "repo_type": "web_app",
    "languages": ["TypeScript"],
    "size": "medium",
    "doc_quality": "high"
  },
  "expected_qualities": {
    "clarity": 5,
    "completeness": 4,
    "specificity": 5,
    "actionability": 4,
    "relevance": 5
  }
}
```

### Custom Quality Rubrics

Modify the rubric in `evaluation_results.json` to add custom criteria:

```json
{
  "rubric": {
    "clarity": "Is the output clear?",
    "security_focus": "Does it identify security issues?",
    "performance_analysis": "Does it analyze performance implications?"
  }
}
```

## Best Practices

1. **Use Diverse Test Cases** - Cover different repository types, sizes, and quality levels
2. **Be Consistent** - Use the same scoring criteria across all test cases
3. **Provide Detailed Feedback** - Explain why you gave each score
4. **Iterate** - Re-run after improvements to validate changes
5. **Track Progress** - Keep tuning sessions organized by version/date

## Integration with CI/CD

Add prompt quality checks to your CI pipeline:

```yaml
# .github/workflows/prompt-quality.yml
- name: Run Prompt Tuning Tests
  run: |
    review-codebase tune init --num-tests 3
    # Run simulations and evaluations
    # Fail if average score < threshold
```

## Related Documentation

- **Archive Documentation**: `archive/PROMPT_TUNING_*.md` - Original methodology
- **Workflow System**: `docs/WORKFLOW_INTEGRATION_PROPOSAL.md` - Workflow design
- **Simulation**: `src/codebase_reviewer/simulation.py` - Simulation engine

## Troubleshooting

### "Evaluation results not found"

Create `evaluation_results.json` based on the template:

```bash
cp evaluation_results_template.json evaluation_results.json
# Edit evaluation_results.json with your scores
```

### Low Scores Across All Criteria

This may indicate:
- Prompts are too vague or generic
- Missing context in prompt templates
- Need for more specific instructions
- Test cases don't match prompt design

Review the improvement recommendations for specific guidance.
